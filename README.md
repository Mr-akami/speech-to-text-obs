# text-to-speech-obs


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