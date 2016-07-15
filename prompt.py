from __future__ import unicode_literals

from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit import prompt
from prompt_toolkit.interface import AbortAction
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.history import FileHistory

import os
from os.path import expanduser

cli_style = style_from_dict({
    Token.Comment:   '#888888 italic',
    Token.Keyword:   '#ff88ff bold',
	Token: '#ff0066'
})

cli_completer = WordCompleter([
    'revert commitid -m [parent number:0,1]',
	'remote -v',
	'remote add branchname repopath',
    'format-patch commit-id --stdout >file.patch',
    'status',
	'stash -p',
	'checkout -p commitid',
	'checkout branchname filepath',
	'commit --amend',
	'rebase -i HEAD~4',
    "log --graph --abbrev-commit --decorate --format=format:'%C(blue)%h%C(reset) - %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset) %C(bold green)%ar%C(reset)'"
], meta_dict={
    'remote -v': 'check remote url',
    'rebase -i HEAD~4': 'interative last 4',
},ignore_case=True)


def main():
	home = expanduser("~")
	our_history = FileHistory(home+'/.git-inter-cli-history')
	try:
		while True:
			text = prompt('$ git ', completer=cli_completer,
						  style=cli_style,complete_while_typing=True,
						  mouse_support=True,history=our_history,
						  on_abort=AbortAction.RETRY)
			os.system("git " + text)
	except EOFError:
		print('exit')
		


if __name__ == '__main__':
    main()
