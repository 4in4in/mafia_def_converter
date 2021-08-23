## Конвертер textdb_xx.def-файлов для mafia ##

Скрипт позволяет сконвертировать файл базы текстов игры __Mafia__ _(textdb_xx.def)_ в обычный текстовый файл для дальнейшего редактирования в текстовых редакторах.

Каждая строка выходного файла имеет следующую структуру:

> `[ ID текста ] <табуляция> [ Текст ]`

## Использование ##

```
usage: main.py [-h] [--i I] [--o O] [--d D]

Script that can convert Mafia textdb_xx.def to txt and txt to textdb_xx.def.

optional arguments:
  -h, --help  show this help message and exit
  --i I       input file (required)
  --o O       output file (required)
  --d D       def2txt or txt2def (required)
```

## Примеры использования ##

__txt => def__

> `python python .\main.py --i="./textdb_en.txt" --o="./textdb_en.def" --d="txt2def"`

__def => txt__

> `python python .\main.py --i="./textdb_en.def" --o="./textdb_en.txt" --d="def2txt"`
