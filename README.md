# text-to-speech-obs

# 使い方
1. nix develop


# 行ったことメモ

1. Nixの利用
   1. pythonのランタイムと、venvの導入。nix develop時に自動でvenvに入る。
      1. c.f. https://github.com/trustbit/nix-whisper-transcription-demo/blob/main/flake.nix
2. フラットパッケージ構造の採用
   1. 小規模だからディレクトリが深くないほうがいいと思って
      1. c.f. https://ramble.impl.co.jp/6178/
3. Linter等の導入. flake8, mypy, black, isort
   1. vscodeのエクステンションを入れた。他に設定はしていない。それぞれが何をするのか知らないが動いているので良し。
      1. c.f. https://qiita.com/siruku6/items/6a8412c41616b558df66
4. hugging face 依存関係インストール
   1. `pip install --upgrade datasets transformers accelerate soundfile librosa evaluate jiwer tensorboard gradio`
      1. c.f. https://huggingface.co/blog/fine-tune-whisper
5. 音声認識
   1. `pip install SpeechRecognition`
   2. so見つからないと言われたので、nix/storeにシンボリックリンク貼ったりした。
      1. これで直っているらしいがまだリリースされてない https://github.com/NixOS/nixpkgs/issues/6860
      2. Derivationを利用してalsa-libとalsa-pluginをまとめたカスタムパッケージを作った。これて一応flake.nixだけで自動化できた
      3. PC再セットアップ時、シンボリックリンクだと循環依存のためエラーがでた。上記との差分はないと思うが、とりあえずファイルコピーした。
   3. 今度はこういったエラー ALSA lib pcm_dsnoop.c:567:(snd_pcm_dsnoop_open) unable to open slave
      1. https://github.com/b-fitzpatrick/cpiped/issues/9 この通りにしてみたがなおらず。もとに戻す。
         1. まだ直せない。Nixを使わずネイティブでセットアップしたがだめ。
         2. 直さなくてよかった。無視していいエラーだった。
   4. libasound_module_rate_samplerate.soが存在していない。以下issueにて改善要望あり
      1. https://github.com/NixOS/nixpkgs/issues/286269
6. リファクタリング
   1. クラスベースに書き直し