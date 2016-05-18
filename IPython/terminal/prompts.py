from pygments.token import Token
import sys

from IPython.core.displayhook import DisplayHook

class Prompts(object):
    def __init__(self, shell):
        self.shell = shell

    def in_prompt_tokens(self, cli=None):
        return [
            (Token.Prompt, 'In ['),
            (Token.PromptNum, str(self.shell.execution_count)),
            (Token.Prompt, ']: '),
        ]

    def _width(self):
        in_tokens = self.in_prompt_tokens()
        return sum(len(s) for (t, s) in in_tokens)

    def continuation_prompt_tokens(self, cli=None, width=None):
        if width is None:
            width = self._width()
        return [
            (Token.Prompt, (' ' * (width - 5)) + '...: '),
        ]

    def rewrite_prompt_tokens(self):
        width = self._width()
        return [
            (Token.Prompt, ('-' * (width - 2)) + '> '),
        ]

    def out_prompt_tokens(self):
        return [
            (Token.OutPrompt, 'Out['),
            (Token.OutPromptNum, str(self.shell.execution_count)),
            (Token.OutPrompt, ']: '),
        ]

class RichPromptDisplayHook(DisplayHook):
    """Subclass of base display hook using coloured prompt"""
    def write_output_prompt(self):
        sys.stdout.write(self.shell.separate_out)
        if self.do_full_cache:
            tokens = self.shell.prompts.out_prompt_tokens()
            if self.shell.pt_cli:
                self.shell.pt_cli.print_tokens(tokens)
            else:
                print(*(s for t, s in tokens), sep='')
