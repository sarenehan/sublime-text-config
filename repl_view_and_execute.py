import sublime_plugin


class ReplViewAndExecute(sublime_plugin.TextCommand):

    def run(self, edit):
        v = self.view
        ex_id = v.scope_name(0).split(" ")[0].split(".", 1)[1]
        lines = v.lines(self.view.sel()[0])  # get the region, ordered
        # get last point (must use v.line)
        last_point = v.line(self.view.sel()[0]).b
        last_line = v.line(last_point)  # get region of last line

        for line in lines:
            self.view.sel().clear()  # clear selection
            self.view.sel().add(line)  # add the first region/line
            text = v.substr(line).strip()
            print('%s' % text)  # prints in console (ctrl+`)

            # ignore empty lines or comments
            if not line.empty() and text[0] != '#':
                v.window().run_command('focus_group',
                                       {"group": 1})  # focus REPL
                v.window().active_view().run_command("insert",
                                                     {"characters": text})
                v.window().run_command('repl_enter')

        # if the last line was empty, hit return
        # else, move the cursor down. check if empty, hit return once more
        if last_line.empty():
            self.view.sel().clear()
            self.view.sel().add(last_line)
            v.window().run_command('focus_group', {"group": 1})  # focus REPL
            v.window().run_command('repl_enter')
            v.window().run_command('focus_group', {"group": 0})
            v.window().run_command('move', {
                "by": "lines",
                "forward": True,
                "extend": False
            })
        else:
            v.window().run_command('focus_group', {"group": 0})
            v.window().run_command('move', {
                "by": "lines",
                "forward": True,
                "extend": False
            })
            if self.empty_space():
                v.window().run_command('focus_group',
                                       {"group": 1})  # focus REPL
                v.window().run_command('repl_enter')

        # move through empty space
        while self.empty_space() and self.eof():
            v.window().run_command('focus_group', {"group": 0})
            v.window().run_command('move', {
                "by": "lines",
                "forward": True,
                "extend": False
            })

    def eof(self):
        v = self.view
        s = v.sel()
        return True if v.line(s[0]).b < v.size() else False

    def empty_space(self):
        v = self.view
        s = v.sel()
        return True if v.line(s[0]).empty() else False
