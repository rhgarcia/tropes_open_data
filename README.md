# Dataset PicTropes

The dataset PicTropes links 5,925 films with 18,270 tropes from the database DBTropes.org.

# Report: Overview of PicTropes, a film trope dataset

(The full article can be found in https://arxiv.org/abs/1809.10959)

The results show the number of tropes in a film goes up to 515 (GuardiansOfTheGalaxy);
however, the average of tropes by film is (43.434) and the
data ts a log-logistic distribution (location=1.945, shape=0.054, scale=29.292).
This distribution is characterized by a long tail and by a mode that is close
to the minimum, that means that all the films tend to have just a dozen
of tropes, and a great minority have hundred of them. In the discussion,
we point out the fact that most of the films with more tropes are superproductions,
a dozen of years old at maximum and in the adventure genre.

Regarding the tropes, the number of films by trope goes up to 1502 (ShoutOut);
however, the average of films by trope is (14.086) and the data ts a folded
Cauchy distribution (location=0.13, shape=1.0, scale=3.735). This distribution
is also characterized by a long tail and by a mode that is close to
the minimum, that means that all the tropes tend to be discovered in a few
films, but a great minority are present un a huge number of films. In the
discussion, we show the need to have a good ontology of tropes so we can
determine the root of the popularity of a small minority of tropes: if they
are just easy to use or if their use correspond to other creative decisions.

This analysis is useful because it can be used together with the dataset Pic-
Tropes to automatically generate plots that follow the canonical appearance
of tropes based on empirical observations, by using data mining and ma-
chine learning techniques. The results will be directly applicable to dierent
researches in the context of the PhD Bio-inspired techniques for procedural
generation of backstories in literature and open world videogames.

Finally, as future work, we could avoid some current limitations of the
dataset PicTropes by adding films meta information (as genre ontology,
votes, popularity or release date) and tropes meta information (as the ease
of application and the eects of this application), so the automatic gen-
eration could lead to plots with higher quality. It would imply retrieving
data from movie databases using dierent techniques and prepare it so it
matches with the tropes and films uniquely. Regarding DBTropes.org, as
its last dump was extracted in 2016, it could be interesting to contribute to
the project in order to have a newer version, with the latests additions and
contributions.

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
