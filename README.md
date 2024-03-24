# text-to-speech-obs

# 使い方

1. nix develop

# 行ったことメモ

1. Nix の利用
   1. python のランタイムと、venv の導入。nix develop 時に自動で venv に入る。
      1. c.f. https://github.com/trustbit/nix-whisper-transcription-demo/blob/main/flake.nix
2. フラットパッケージ構造の採用
   1. 小規模だからディレクトリが深くないほうがいいと思って
      1. c.f. https://ramble.impl.co.jp/6178/
3. Linter 等の導入. flake8, mypy, black, isort
   1. vscode のエクステンションを入れた。他に設定はしていない。それぞれが何をするのか知らないが動いているので良し。
      1. c.f. https://qiita.com/siruku6/items/6a8412c41616b558df66
4. hugging face 依存関係インストール
   1. `pip install --upgrade datasets transformers accelerate soundfile librosa evaluate jiwer tensorboard gradio`
      1. c.f. https://huggingface.co/blog/fine-tune-whisper
5. 音声認識
   1. `pip install SpeechRecognition`
   2. so 見つからないと言われたので、nix/store にシンボリックリンク貼ったりした。
      1. これで直っているらしいがまだリリースされてない https://github.com/NixOS/nixpkgs/issues/6860
      2. Derivation を利用して alsa-lib と alsa-plugin をまとめたカスタムパッケージを作った。これて一応 flake.nix だけで自動化できた
      3. PC 再セットアップ時、シンボリックリンクだと循環依存のためエラーがでた。上記との差分はないと思うが、とりあえずファイルコピーした。
   3. 今度はこういったエラー ALSA lib pcm_dsnoop.c:567:(snd_pcm_dsnoop_open) unable to open slave
      1. https://github.com/b-fitzpatrick/cpiped/issues/9 この通りにしてみたがなおらず。もとに戻す。
         1. まだ直せない。Nix を使わずネイティブでセットアップしたがだめ。
         2. 直さなくてよかった。無視していいエラーだった。
   4. libasound_module_rate_samplerate.so が存在していない。以下 issue にて改善要望あり
      1. https://github.com/NixOS/nixpkgs/issues/286269
6. リファクタリング
   1. クラスベースに書き直し
7. https://github.com/ketman55/whisper-mic-for-dominion/blob/main/mic.py を参考に recognizer を記載
8. 依存を pip でインストール

- https://dev.classmethod.jp/articles/whisper-fine-tuning-by-huggingface/　を参考
  - pip install datasets
  - pip install git+https://github.com/huggingface/transformers
  - pip install libsora
  - pip install evaluate
  - pip install jiwer
  - pip install gradio

9. 実行したら RuntimeError: Found no NVIDIA driver on your system. Please check that you have an NVIDIA GPU and installed a driver from http://www.nvidia.com/Download/index.aspxのエラーがでた。
   - nvidia-smi でみても Driver はインストールされている。とりあえず CPU モードで試す
10. CPU モードで試すとうまく認識できたがとても遅い。

11. GPU が認識されないのは nix のせい。Cuda を認識していない。

- python311Packages.torchWithCuda を追加した \* このままだとインストールできななかったので、ホストで`export NIXPKGS_ALLOW_UNFREE=1`をし、`nix deveop --impure`で host の環境変数を持ってきた。nix でお手軽環境構築から離れていてとても気持ちが悪い。うまく言ったとしても代替手段を見つけないといけない。
  こんな感じでかけるらしい。

```nix
     {
  description = "A flake for a nix shell environment with both free and unfree packages";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: {
    devShell.x86_64-linux = let
      # カスタマイズされたnixpkgsのインスタンスを生成します。
      customPkgs = import nixpkgs {
        config = {
          allowUnfreePredicate = pkg: builtins.elem (lib.getName pkg) [
            "nvidia-x11-550.54.14-6.6.18"  # ここに非フリーパッケージを追加
          ];
        };
      };
    in nixpkgs.legacyPackages.x86_64-linux.mkShell {
      buildInputs = with nixpkgs.legacyPackages.x86_64-linux; [
        # ここに普通のフリーパッケージを追加
        git
        vim
      ] ++ with customPkgs; [
        # ここに非フリーパッケージを追加
        nvidia-x11-550.54.14-6.6.18
      ];
    };
  };
}
```

12. faster_whisper を入れてみた

- GPU はメモリが足りない。CPU モードだとおそすぎる。
