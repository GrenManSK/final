import logging


class SimpleCompleter(object):
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        """
        The complete function is called as complete(text, state), for state in 0, 1, 2, ...
        until it returns a non-string value. It should return the next possible completion starting with 'text'.

        :param self: Represent the instance of the class
        :param text: Filter the list of options
        :param state: Keep track of the index in the matches list
        :return: The state'th item from the match list, if we have that many
        """
        response = None
        if state == 0:
            if text:
                self.matches = [s for s in self.options if s and s.startswith(text)]
                logging.debug("%s matches: %s", repr(text), self.matches)
            else:
                self.matches = self.options[:]
                logging.debug("(empty input) matches: %s", self.matches)

        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        logging.debug("complete(%s, %s) => %s", repr(text), state, repr(response))
        return response


# ----------------------------------------------------------------
#
# Example usage
#
# import readline
# readline.set_completer(
#     SimpleCompleter(['example1', 'example2']).complete)
# readline.parse_and_bind('tab: complete')
