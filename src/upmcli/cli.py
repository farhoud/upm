from click import command, echo

ascii_snek = """\
    --..,_                     _,.--.
       `'.'.                .'`__ o  `;__.
          '.'.            .'.'`  '---'`  `
            '.`'--....--'`.'
              `'--....--'`
"""

@command()
def main():
    echo(ascii_snek)
    
if __name__ == '__main__':
    main()
