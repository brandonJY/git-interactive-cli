from __future__ import unicode_literals

from six import string_types
from prompt_toolkit.completion import Completer, Completion
import subprocess


__all__ = (
    'GitCompleter',
)


class GitCompleter(Completer):
    """
    Simple autocompletion on a list of words.

    :param words: List of words.
    :param ignore_case: If True, case-insensitive completion.
    :param meta_dict: Optional dict mapping words to their meta-information.
    :param WORD: When True, use WORD characters.
    :param sentence: When True, don't complete by comparing the word before the
        cursor, but by comparing all the text before the cursor. In this case,
        the list of words is just a list of strings, where each string can
        contain spaces. (Can not be used together with the WORD option.)
    :param match_middle: When True, match not only the start, but also in the
                         middle of the word.
    """
    def __init__(self, words, ignore_case=False, meta_dict=None, WORD=False,
                 sentence=False, match_middle=False):
        assert not (WORD and sentence)

        self.words = list(words)
        self.ignore_case = ignore_case
        self.meta_dict = meta_dict or {}
        self.WORD = WORD
        self.sentence = sentence
        self.match_middle = match_middle
        assert all(isinstance(w, string_types) for w in self.words)

    def get_branch_list(self):
        branch_list=subprocess.check_output('git branch', shell=True).replace('\r','').replace('\n','').split('  ')
        return branch_list

    def get_commit_list(self):
        commit_list=subprocess.check_output('git log --pretty=oneline --abbrev-commit', shell=True).split('\n')
        return commit_list

    def git_command_match(self,txt,search_pattern):
        txt_list=txt.split(' ')
        search_pattern_list=search_pattern.split(' ')
        loop_length=min(len(txt_list),len(search_pattern_list))
        for i in range(loop_length):
            if search_pattern_list[i]!='[branchname]' and search_pattern_list[i]!='[commitid]' :
                if not search_pattern_list[i].startswith(txt_list[i]) :
                    return False
        return True

    def match_start_pos(self,txt,search_pattern):
        txt_list=txt.split(' ')
        search_pattern_list=search_pattern.split(' ')
        search_pattern_new=''
        for i in range(len(txt_list)-1):
            search_pattern_new+=' '+search_pattern_list[i]
        return len(search_pattern_new)

    def get_completions(self, document, complete_event):
        # Get word/text before cursor.
        if self.sentence:
            word_before_cursor = document.text_before_cursor
        else:
            word_before_cursor = document.get_word_before_cursor(WORD=self.WORD)

        if self.ignore_case:
            word_before_cursor = word_before_cursor.lower()

        def word_matches(word):
            """ True when the word before the cursor matches. """
            if self.ignore_case:
                word = word.lower()

            if self.match_middle:
                return word_before_cursor in word
            else:
                #return word.startswith(word_before_cursor)
                return self.git_command_match(word_before_cursor,word)
				
        for a in self.words:
            if word_matches(a):
                display_meta = self.meta_dict.get(a, '')
                if a.startswith('[branchname]',self.match_start_pos(word_before_cursor,a)):
                    for branch_name in self.get_branch_list():
                        yield Completion(word_before_cursor+branch_name.replace('* ',''), -len(word_before_cursor),display=branch_name, display_meta=a)

                elif a.startswith('[commitId]',self.match_start_pos(word_before_cursor,a)):
                    for commit_list in self.get_commit_list():
                        yield Completion(word_before_cursor+commit_list.split(' ')[0], -len(word_before_cursor),display=commit_list, display_meta=a)
                else:
                    yield Completion(a, -len(word_before_cursor), display_meta=display_meta)
