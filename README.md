# CPAssistant

Cantonese pronunciation assistant.

## Usage

```Batchfile
python cp_assist.py [-h] [-v] [-f FILE] [-s STR]

Convert Chinese to Cantonese.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -f FILE, --file FILE  file path
  -s STR, --str STR     chinese string
  -p FILE, --pdf FILE   output PDF file path
```

## Examples

```Batchfile
python cp_assist.py -s "大家好，我们来做一个注音测试"
```

Or

```Batchfile
python cp_assist.py -f /file/path -p /output/file/path.pdf
```

## Dependencies

* [jieba](https://github.com/fxsjy/jieba): Chinese text segmentation.
* [chardet](https://github.com/chardet/chardet): Universal encoding detector for Python 2 and 3
* [CantoneseDict](https://github.com/Ho1iarty/CantoneseDict): A tool for creating a Cantonese dictionary(jyutping).
* [reportlab](https://pypi.org/project/reportlab/): Create PDF files.

## Update

* 2022-10-17(Mon):
  * Support output PDF file
  * Refine documents

* 2014-10-27(Mon):
  * Add encoding detector
  * Add examples

* 2014-04-22(Tue):
  * Start project.
  * Add file **lyrics** for test.
  * To be continued.
