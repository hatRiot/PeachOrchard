from abc import ABCMeta, abstractmethod
import src.core.utility as utility


class Fuzzer:
    """ Defines the interface that a fuzzer must implement to
    fit nicely in with the crowd.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self.name = "Generic Fuzzer"
        self.crashes = {}

    @abstractmethod
    def fetch_crashes(self):
        """ Returns a dictionary of all crashes in the format
        {crash_idx : crash_file_path}
        """

        raise NotImplementedError


    @abstractmethod
    def get_status(self):
        """ Returns the fuzzer's current status.  This may differ
        from fuzzer to fuzzer, as some return progress (200/400),
        current cycle, or something else entirely.  This should be
        a string of some kind.
        """

        raise NotImplementedError


    @abstractmethod
    def check_session(self):
        """
        """

        raise NotImplementedError


    def check_new_crashes(self):
        """ Returns a dictionary of any new crashes since last refresh
        of the crashes.
        """

        update = self.fetch_crashes()
        if len(update) != len(self.crashes):
            
            # new crashes
            update = utility.dict_delta(update, self.crashes)
            self.crashes = dict(self.crashes.items() + update.items())

        else:
            update = None

        return update
