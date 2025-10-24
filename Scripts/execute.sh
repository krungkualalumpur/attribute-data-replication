export PYTHONPATH=src

INPUT=$1
OUTPUT_FILE_PATH=$2

. Scripts/setup.sh
python -m data_parser "$INPUT" "$OUTPUT_FILE_PATH"

echo $OUTPUT_FILE_PATH