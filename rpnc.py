#!/usr/bin/env python
#coding: utf8

# Copyright (C) 2011 by Stefano Palazzo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import gtk
import pango
import math

class RPNC (object):

    stack = [0.0, 0.0]
    disp = ""
    last_x = 0.0
    store = 0.0

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("/opt/apps/rpnc/rpnc.glade")
        self.builder.connect_signals(self)
        self.builder.get_object("label3").modify_font(
            pango.FontDescription("UbuntuMono"))
        self.builder.get_object("label4").modify_font(
            pango.FontDescription("UbuntuMono"))
        self.builder.get_object("viewport1").modify_bg(gtk.STATE_NORMAL,
            gtk.gdk.color_parse("white"))
        self.update()

    def enter(self, widget):
        if self.disp:
            self.stack.append(float(self.disp))
        self.disp = ""
        self.builder.get_object("label5").set_label("")
        self.update()

    def swap(self, widget):
        if self.disp:
            self.enter(widget)
        if len(self.stack) >= 2:
            self.stack[-2], self.stack[-1] = self.stack[-1], self.stack[-2]
        self.disp = ""
        self.update()

    def rup(self, widget):
        if self.disp:
            self.enter(widget)
        if len(self.stack) >= 2:
                self.stack.append(self.stack.pop(0))
        self.disp = ""
        self.update()

    def rdn(self, widget):
        if self.disp:
            self.enter(widget)
        if len(self.stack) >= 2:
            self.stack.insert(0, self.stack.pop(-1))
        self.disp = ""
        self.update()

    def delete(self, widget):
        if self.disp:
            self.enter(widget)
        if self.stack:
            self.stack = self.stack[:-1]
        self.disp = ""
        self.update()

    def separator(self, widget):
        if not "." in self.disp:
            self.disp += "."
        self.update()

    def divide(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            if len(self.stack) >= 2:
                self.stack.append(self.stack.pop(-2) / self.stack.pop(-1))
            self.disp = ""
        except Exception as e:
            self.builder.get_object("label5").set_label(str(e))
            self.stack.append(float('nan'))
        else:
            self.builder.get_object("label5").set_label("")
        finally:
            self.update()

    def multiply(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            if len(self.stack) >= 2:
                self.stack.append(self.stack.pop(-2) * self.stack.pop(-1))
            self.disp = ""
        except Exception as e:
            self.builder.get_object("label5").set_label(str(e))
            self.stack.append(float('nan'))
        else:
            self.builder.get_object("label5").set_label("")
        finally:
            self.update()

    def subtract(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            if len(self.stack) >= 2:
                self.stack.append(self.stack.pop(-2) - self.stack.pop(-1))
            self.disp = ""
        except Exception as e:
            self.builder.get_object("label5").set_label(str(e))
            self.stack.append(float('nan'))
        else:
            self.builder.get_object("label5").set_label("")
        finally:
            self.update()

    def add(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            if len(self.stack) >= 2:
                self.stack.append(self.stack.pop(-2) + self.stack.pop(-1))
            self.disp = ""
        except Exception as e:
            self.builder.get_object("label5").set_label(str(e))
            self.stack.append(float('nan'))
        else:
            self.builder.get_object("label5").set_label("")
        finally:
            self.update()

    def nine(self, widget):
        self.disp += "9"
        self.update()

    def eight(self, widget):
        self.disp += "8"
        self.update()

    def seven(self, widget):
        self.disp += "7"
        self.update()

    def six(self, widget):
        self.disp += "6"
        self.update()

    def five(self, widget):
        self.disp += "5"
        self.update()

    def four(self, widget):
        self.disp += "4"
        self.update()

    def three(self, widget):
        self.disp += "3"
        self.update()

    def two(self, widget):
        self.disp += "2"
        self.update()

    def one(self, widget):
        self.disp += "1"
        self.update()

    def zero(self, widget):
        self.disp += "0"
        self.update()

    def mod(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            if len(self.stack) >= 2:
                self.stack.append(self.stack.pop(-2) % self.stack.pop(-1))
            self.disp = ""
        except Exception as e:
            self.builder.get_object("label5").set_label(str(e))
            self.stack.append(float('nan'))
        else:
            self.builder.get_object("label5").set_label("")
        finally:
            self.update()

    def floor(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            if self.stack:
                self.stack.append(float(int(self.stack.pop(-1))))
            self.disp = ""
        except Exception as e:
            self.builder.get_object("label5").set_label(str(e))
            self.stack.append(float('nan'))
        finally:
            self.update()

    def reciprocal(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            if self.stack:
                self.stack.append(1 / self.stack.pop(-1))
            self.disp = ""
        except Exception as e:
            self.builder.get_object("label5").set_label(str(e))
            self.stack.append(float('nan'))
        else:
            self.builder.get_object("label5").set_label("")
        finally:
            self.update()

    def log(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            if self.stack:
                self.stack.append(math.log10(self.stack.pop(-1)))
            self.disp = ""
        except Exception as e:
            self.builder.get_object("label5").set_label(str(e))
            self.stack.append(float('nan'))
        else:
            self.builder.get_object("label5").set_label("")
        finally:
            self.update()

    def ln(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            if self.stack:
                self.stack.append(math.log(self.stack.pop(-1)))
            self.disp = ""
        except Exception as e:
            self.builder.get_object("label5").set_label(str(e))
            self.stack.append(float('nan'))
        else:
            self.builder.get_object("label5").set_label("")
        finally:
            self.update()

    def power(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            if len(self.stack) >= 2:
                self.stack.append(self.stack.pop(-2) ** self.stack.pop(-1))
            self.disp = ""
        except Exception as e:
            self.builder.get_object("label5").set_label(str(e))
            self.stack.append(float('nan'))
        else:
            self.builder.get_object("label5").set_label("")
        finally:
            self.update()

    def square_root(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            if self.stack:
                self.stack.append(self.stack.pop(-1) ** 0.5)
            self.disp = ""
        except Exception as e:
            self.builder.get_object("label5").set_label(str(e))
            self.stack.append(float('nan'))
        else:
            self.builder.get_object("label5").set_label("")
        finally:
            self.update()

    def square(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            if self.stack:
                self.stack.append(self.stack.pop(-1) ** 2)
            self.disp = ""
        except Exception as e:
            self.builder.get_object("label5").set_label(str(e))
            self.stack.append(float('nan'))
        else:
            self.builder.get_object("label5").set_label("")
        finally:
            self.update()

    def fact(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            if self.stack:
                self.stack.append(float(math.factorial(self.stack.pop(-1))))
            self.disp = ""
        except Exception as e:
            self.builder.get_object("label5").set_label(str(e))
            self.stack.append(float('nan'))
        else:
            self.builder.get_object("label5").set_label("")
        finally:
            self.update()

    def last(self, widget):
        if self.disp:
            self.enter(widget)
        self.disp = ""
        self.stack.append(self.last_x)
        self.update()

    def recall(self, widget):
        if self.disp:
            self.enter(widget)
        self.disp = ""
        self.stack.append(self.store)
        self.update()

    def store(self, widget):
        if self.disp:
            self.enter(widget)
        self.disp = ""
        if self.stack:
            self.store = self.stack[-1]
        else:
            self.store = 0.0
        self.update()

    def chs(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            if self.stack:
                self.stack.append(-self.stack.pop(-1))
            self.disp = ""
            self.update()
        except Exception as e:
            self.builder.get_object("label5").set_label(str(e))
            self.stack.append(float('nan'))
        else:
            self.builder.get_object("label5").set_label("")
        finally:
            self.update()

    def pi(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            self.stack.append(math.pi)
            self.disp = ""
            self.update()
            self.builder.get_object("label5").set_label("")
        finally:
            self.update()

    def e(self, widget):
        try:
            if self.disp:
                self.enter(widget)
            self.last_x = self.stack[-1]
            self.stack.append(math.e)
            self.disp = ""
            self.update()
            self.builder.get_object("label5").set_label("")
        finally:
            self.update()

    def backspace(self, widget):
        self.disp = self.disp[:-1]
        self.update()

    def update(self):
        while len(self.stack) < 2:
            self.stack.insert(0, 0.0)
        if self.disp:
            self.builder.get_object("label3").set_label(self.disp)
        else:
            self.builder.get_object("label3").set_label(str(self.stack[-1]))
            self.builder.get_object("label4").set_label(str(self.stack[-2]))

    def on_window1_key_press_event(self, widget, data):
        if data.keyval == 65288:  # backspace
            self.disp = self.disp[:-1]
        self.update()

    def about(self, widget):
        about = gtk.AboutDialog()
        about.set_program_name("RPN Calculator")
        about.set_version("0.1")
        about.set_copyright("Copyright 2011 Stefano Palazzo")
        about.set_comments("A Stack-Based IEEE 754 Double "
            "Precision RPN Calculator")
        about.set_website("http://www.plzz.de/")
        about.set_logo_icon_name("accessories-calculator")
        about.run()
        about.destroy()

    def run(self, *args):
        gtk.main()

    def quit(self, *args):
        gtk.main_quit()

if __name__ == '__main__':
    RPNC().run()
