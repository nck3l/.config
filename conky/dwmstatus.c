/*
 * Simple C program to use Conky to set status information in dwm.
 * compile the code with: gcc dwmstatus.c -lX11 -o dwmstatus
 *
 * and move/link dwmstatus to a directory in your $PATH (e.g. ~/.local/bin/)
 *
 * call or add to your init script: conky | dwmstatus
 *
 * Taken straight from the Arch Wiki:
 * https://wiki.archlinux.org/title/Dwm#Conky_statusbar
*/

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <X11/Xlib.h>

int main(int argc, char * argv[])
{
        Display * dpy = NULL;
        Window win = 0;
        size_t length = 0;
        ssize_t bytes_read = 0;
        char * input = NULL;

        dpy = XOpenDisplay(getenv("DISPLAY"));
        if (dpy == NULL)
        {
                fprintf(stderr, "Can't open display, exiting.\n");
                exit(1);
        }
        win = DefaultRootWindow(dpy);

        while ((bytes_read = getline(&input, &length, stdin)) != EOF)
        {
                input[strlen(input) - 1] = '\0';
                XStoreName(dpy, win, input);
                XFlush(dpy);
                fprintf(stderr, "Input: %s", input);
                fprintf(stderr, "\nbytes read: %ld\n", bytes_read);
        }
        free(input);
        return 0;
}
