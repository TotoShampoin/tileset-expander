# Tileset Expander

This is a simple python script for your tilesets, following the patterns provided by Godot.

It'll take in a tileset like this:  
![input](https://docs.godotengine.org/en/3.5/_images/autotile_template_2x2.png)

And output a tileset like this:  
![output](https://docs.godotengine.org/en/3.4/_images/autotile_template_3x3_minimal.png)

## Usage

First, ensure you have the requirements

```sh
pip install -r requirements.txt
```

```sh
python tileset-expander.py -i input.png -o output.png
```

You may also use various options, though they don't actually do anything to the final result. See `python tileset-expander.py -h` for more informations.

## WHERE'S THE EXE

Check out the Releases section on the right if you really want _~ the exe ~_
