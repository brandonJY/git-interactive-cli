from __future__ import unicode_literals

from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit import prompt
from prompt_toolkit.interface import AbortAction
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.history import FileHistory

import subprocess
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
    'remote set-url branchname repopath',
    'format-patch commit-id --stdout >file.patch',
    'status',
    'stash save -p message',
    'checkout -p commitid',
    'checkout branchname filepath',
    'checkout branchname',
    'commit --amend',
    'rebase -i HEAD~4',
    'rebase -i --root',
    'cherry-pick commitid',
    "filter-branch --env-filter 'GIT_COMMITTER_DATE=$GIT_AUTHOR_DATE; export GIT_COMMITTER_DATE",
    "log --graph --abbrev-commit --decorate --format=format:'%C(blue)%h%C(reset) - %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset) %C(bold green)%ar%C(reset)'"
], meta_dict={
	'checkout branchname':'switch branch',
    'remote -v': 'check remote url',
    'rebase -i HEAD~4': 'interative last 4',
    'remote set-url branchname repopath':'remote set-url origin https://github.com/REPOSITORY.git'
},ignore_case=True)


def main():
	home = expanduser("~")
	git_history = FileHistory(home+'/.git-inter-cli-history')
	try:
		while True:
	
			currentBranchName=subprocess.check_output('git name-rev --name-only HEAD', shell=True)
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
