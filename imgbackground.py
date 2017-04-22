import base64
import curses
import errno
import fcntl
import time
import imghdr
import os
import struct
import sys
from subprocess import Popen, PIPE
from ranger.core.shared import FileManagerAware

class ImageDisplayer(object):
    """Image display provider functions for drawing images in the terminal"""

    def draw(self, path, start_x, start_y, width, height):
        """Draw an image at the given coordinates."""
        pass

    def clear(self, start_x, start_y, width, height):
        """Clear a part of terminal display."""
        pass

    def quit(self):
        """Cleanup and close"""
pass
class URXVTImageDisplayer(ImageDisplayer, FileManagerAware):
    """Implementation of ImageDisplayer working by setting the urxvt
    background image "under" the preview pane.
    Ranger must be running in urxvt for this to work.
    """

    def __init__(self):
        self.display_protocol = "\033"
        self.close_protocol = "\a"
        if "screen" in os.environ['TERM']:
            print "ohh"
            self.display_protocol += "Ptmux;\033\033"
            self.close_protocol += "\033\\"
        self.display_protocol += "]20;"

    @staticmethod
    def _get_max_sizes():
        """Use the whole terminal."""
        pct_width = 100
        pct_height = 100
        return pct_width, pct_height

    @staticmethod
    def _get_centered_offsets():
        """Center the image."""
        pct_x = 50
        pct_y = 50
        return pct_x, pct_y

    def _get_sizes(self):
        """Return the width and height of the preview pane in relation to the
        whole terminal window.
        """
        # if self.fm.ui.pager.visible:
            # return self._get_max_sizes()

        # total_columns_ratio = sum(self.fm.settings.column_ratios)
        # preview_column_ratio = self.fm.settings.column_ratios[-1]
        # pct_width = int((100 * preview_column_ratio) / total_columns_ratio)
        # pct_height = 100  # As much as possible while preserving the aspect ratio.
        # return pct_width, pct_height
        return 20,20

    def _get_offsets(self):
        """Return the offsets of the image center."""
        # if self.fm.ui.pager.visible:
            # return self._get_centered_offsets()

        pct_x = 100  # Right-aligned.
        pct_y = 2    # TODO: Use the font size to calculate this offset.
        return pct_x, pct_y

    def draw(self, path, start_x, start_y, width, height):
        # The coordinates in the arguments are ignored as urxvt takes
        # the coordinates in a non-standard way: the position of the
        # image center as a percentage of the terminal size. As a
        # result all values below are in percents.

        pct_x, pct_y = self._get_offsets()
        pct_width, pct_height = self._get_sizes()

        sys.stdout.write(
                self.display_protocol +
                path +
                ";{pct_width}x{pct_height}+{pct_x}+{pct_y}:op=keep-aspect".format(
                    pct_width=pct_width, pct_height=pct_height, pct_x=pct_x, pct_y=pct_y
                    ) +
                self.close_protocol
                )
        sys.stdout.flush()

    def clear(self, start_x, start_y, width, height):
        sys.stdout.write(
                self.display_protocol +
                ";100x100+1000+1000" +
                self.close_protocol
                )
        sys.stdout.flush()

    def quit(self):
        self.clear(0, 0, 0, 0)  # dummy assignments

if __name__ == "__main__":
    u=URXVTImageDisplayer()
    u.draw('/home/sourya/pro/bakchodhi/temp/6nxvoyp5JJQ.jpg',100,100,320,180)
    time.sleep(2)
    u.clear(0,0,320,180)
    

    
