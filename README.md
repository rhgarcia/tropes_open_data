# tropes_open_data

You need to install Python 3 first.

Get `invoke` 

    pip install -e git+https://github.com/pyinvoke/invoke#egg=invoke

Install required libraries

    pip install scipy matplotlib


Install `pweave`

    pip install --upgrade Pweave

Use it to generate the document from the command line

```
> invoke clean build open-pdf
```

If you want to edit .texw in your favorite editor, well, you're out of luck, because I couldn't find a way to make it work in emacs.

However, you can use this in Atom:

    apm install language-weave Hydrogen
