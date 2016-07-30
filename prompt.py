from __future__ import unicode_literals

from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit import prompt
from prompt_toolkit.interface import AbortAction
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.history import FileHistory

import subprocess
from os.path import expanduser
import json

cli_style = style_from_dict({
    Token.Comment:   '#888888 italic',
    Token.Keyword:   '#ff88ff bold',
	Token: '#ff0066'
})

with open('git_command.json', 'r') as f:
	git_command=json.load(f)
cli_completer = WordCompleter(git_command.keys(), meta_dict=git_command,ignore_case=True)


def main():
	home = expanduser("~")
	git_history = FileHistory(home+'/.git-inter-cli-history')
	try:
		while True:
	
			currentBranchName=subprocess.check_output('git rev-parse --abbrev-ref HEAD', shell=True)
			currentPath=subprocess.check_output('pwd')
			print(currentPath.replace('\n','')+' ('+currentBranchName.replace('\n','')+')')
	
			text = prompt('$ git ', completer=cli_completer,
						  style=cli_style,complete_while_typing=True,
						  mouse_support=True,history=git_history,
						  on_abort=AbortAction.RETRY)
			if text=='q':
				while True:
					text=prompt('$ ',style=cli_style)
					if text=='git':
						break
					os.system(text)
			elif text=='':
				continue
			else:
				status=subprocess.call("git " + text, shell=True)
	except EOFError:
		print('exit')
		


if __name__ == '__main__':
    main()
