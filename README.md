# Extract Video File Metadata / 動画ファイルのメタデータを抽出

EN

Extracts metadata from video files in a specified directory, including information such as frame rate, duration, bit rate, and whether the file contains audio. Saves the metadata as a JSON file.

JP

指定したディレクトリ内の動画ファイルからメタデータ（フレームレート、再生時間、ビットレート、音声ストリームの有無など）を抽出し、JSONファイルとして保存します。

## Environment / 環境

* Python 3.12.0
* ffmpeg-python 0.2.0

## Usage / 使い方

EN

Install Library form requirements.txt.

JP

requirements.txtからライブラリをインストール

```shell
pip install -r requirements.txt
```

## Sample usage / 実行方法

EN

Place the target video files in the specified directory, then run the script to extract metadata. The metadata will be saved to a JSON file.

JP

対象となる動画ファイルを指定したディレクトリに配置し、スクリプトを実行してメタデータを抽出します。抽出したメタデータはJSONファイルに保存されます。

```shell
python metadata.py
```

## Results / 出力結果

EN

The extracted metadata is saved in a file named `metadata.json`. Here is an example of the JSON structure:

JP

抽出されたメタデータは`metadata.json`というファイルに保存されます。JSONの構造は以下のとおりです。

```json
[
    {
        "file_name": "example.mp4",
        "extension": ".mp4",
        "has_audio": true,
        "frame_rate": 29.97,
        "duration": "2分34秒",
        "bit_rate": "1200000"
    },
    {
        "file_name": "example2.avi",
        "extension": ".avi",
        "has_audio": false,
        "frame_rate": 29.97,
        "duration": "3分10秒",
        "bit_rate": "Unknown"
    }
]
```

EN

This data provides details about each video file, including its filename, extension, presence of audio, frame rate, duration, and bit rate.

JP

JSONデータには、各動画ファイルの詳細（ファイル名、拡張子、音声の有無、フレームレート、再生時間、ビットレート）が含まれています。

## Notes / 注意事項

EN

- Make sure that `ffmpeg` is installed.
- The directory path and output file path are hardcoded in the script. You can modify the variables `DIRECTORY_PATH` and `OUTPUT_JSON` as needed.

JP

- `ffmpeg`がインストールされていることを確認してください。
- スクリプト内のディレクトリパスと出力ファイルパスは固定値でスクリプト内に設定されています。必要に応じて、`DIRECTORY_PATH` と `OUTPUT_JSON` の値を変更してください。

## Author / 作成者

- [Fantom, Inc. (JP)](https://twitter.com/Fantomcojp)
