Gitlab CI Tools
===============
.. badges-start


.. image:: https://gitlab.com/jbweston/gitlab-ci-tools/badges/master/build.svg
   :target: https://gitlab.com/jbweston/gitlab-ci-tools/badges/master/build.svg
   :alt: Build status

.. image:: https://img.shields.io/pypi/l/gitlab-ci-tools.svg
   :target: https://img.shields.io/pypi/l/gitlab-ci-tools.svg
   :alt: License

.. image:: https://img.shields.io/pypi/v/gitlab-ci-tools.svg
   :target: https://img.shields.io/pypi/v/gitlab-ci-tools.svg
   :alt: PyPi package

.. badges-end

Scripts for getting useful information (e.g. the git hash of the last successful build) from within Gitlab CI 

Overview
--------
Often when using Gitlab CI you need information that is not
available from the `environment variables`_ provided by the CI
runner. This package contains a collection of scripts for obtaining
information from the Gitlab API

.. _environment variables: https://docs.gitlab.com/ce/ci/variables/

License
-------
``gitlab-ci-tools`` is licensed under the simplfied (2-clause) BSD licence.
See the LICENSE_ file for details.

.. _LICENSE: LICENSE

Installation
------------
The scripts are written in Python 3, so this will need to be installed
prior to the following::

    pip3 install gitlab-ci-tools

You can install the package on your local computer to test out
the scripts (see the Usage section for details), however typically
you will want to install this package into the Gitlab CI environment.

The simplest way to accomplish this is to add the following to the top
of your ``.gitlab-ci.yml``::

    before_script:
        - pip3 install gitlab-ci-tools


Usage
-----
Installing ``gitlab-ci-tools`` installs a bunch of scripts that you can
run from the command line. See the next section for a list of the installed
tools.

In order for the scripts to be able to access the Gitlab API you must
provide a CI secret variable ``GITLAB_API_TOKEN`` that contains a
personal access token with ``api`` scope (check out `these instructions`_ to
find out how to generate one).

Security Considerations
~~~~~~~~~~~~~~~~~~~~~~~

Unfortunately Gitlab's API permissions are not very granular, so
**anyone with access to this token is, effectively, you** (at least as
far as Gitlab is concerned). If people you don't trust have access to
your CI (e.g. they can make CI-triggering commits to your repository)
**this is a bad idea**. There are several outstanding issues on Gitlab
(e.g. `#29566`_ and `#41084`_) that attempt to address the problem of
authenticated API access from within CI runners.

.. _these instructions: https://docs.gitlab.com/ce/user/profile/personal_access_tokens.html#creating-a-personal-access-token
.. _#29566: https://gitlab.com/gitlab-org/gitlab-ce/issues/29566
.. _#41084: https://gitlab.com/gitlab-org/gitlab-ce/issues/41084

List of Tools
-------------

``last-good-build``
~~~~~~~~~~~~~~~~~~~
Print the Git hash of the last successful build for the current branch.
An useful example would be generating a PDF of the diff between two Latex
documents::

    before_script:
      pip install gitlab-ci-tools
      LAST_GOOD_BUILD=$(last-good-build || echo '')

    report diff:
      script:
        - git show $LAST_GOOD_BUILD:important_doc.tex > old_doc.tex
        - latexdiff old_doc.tex important_doc.tex > diff_doc.tex
        - latexmk -pdf diff_doc.tex
      artifacts:
        paths:
          - diff_doc.pdf

Contributing
------------
I would be happy to add more tools here, not just ones that I find useful.
It would be good if the script were to follow a similar structure to the
existing ones (i.e. provide a ``main()`` function, and expose a command line
that can be driven with command-line options or with environment variables),
but I am happy to guide anyone through this process if need be.

Once there is more than a single script we can start to think about how best
to separate out common functionlity so that we can reduce boilerplate.
