INPUT=Scripts/input_template.json
OUTPUT_DIR=output/exe_out
OUTPUT_FILE_NAME=output.luau #prevents treating output.luau as a folder instead of a luau file

OUTPUT_FILE_PATH="$OUTPUT_DIR/$OUTPUT_FILE_NAME"

# touch "$OUTPUT_FILE_PATH"

. Scripts/setup.sh
python app/__main__.py "$INPUT" "$OUTPUT_FILE_PATH"

echo $OUTPUT_FILE_PATH