# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will give us the cleaning logic.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: enable=line-too-long
import PyFunceble
from PyFunceble.helpers import File


class Clean:
    """
    Provide the cleaning logic.

    .. note::
        By cleaning we mean the cleaning of the :code:`output` directory.

    :param list_to_test: The list of domains we are testing.
    :type list_to_test: list|None

    :param bool clean_all:
        Tell the subsystem if we need to clean all.
        Which include, of course, the output directory but also
        all other file(s) generated by our system.
    """

    def __init__(self, list_to_test, clean_all=False):
        if list_to_test:
            # The list to test is not empty.

            try:
                # We try to see if we have to reset counters and clean the output directory.

                # We get the number of tested.
                number_of_tested = PyFunceble.INTERN["counter"]["number"]["tested"]

                if (
                    number_of_tested == 0
                    or list_to_test[number_of_tested - 1] == list_to_test[-1]
                    or number_of_tested >= len(list_to_test)
                ):
                    # * If the number of tested is null,
                    # or
                    # * the last tested element is the same as the last element in the
                    #   sequence,
                    # or
                    # * The number of tested is equal to the number of elements in the
                    #   sequence,

                    # We reset the counters.
                    PyFunceble.Preset.reset_counters()

                    # We clean the output directory.
                    self.almost_everything(clean_all)
            except IndexError:
                # But if at any time in the conditionnal an Index Error occurs,

                # We reset the counters.
                PyFunceble.Preset.reset_counters()

                # We clean the output directory.
                self.almost_everything(clean_all)
        else:
            # The list to test is empty.

            # We clean the output directory.
            self.almost_everything(clean_all)

    @classmethod
    def file_to_delete(cls):
        """
        Return the list of file to delete.
        """

        # We initiate the directory we have to look for.
        directory = "{0}{1}".format(
            PyFunceble.OUTPUT_DIRECTORY, PyFunceble.OUTPUTS["parent_directory"]
        )

        if not directory.endswith(PyFunceble.directory_separator):  # pragma: no cover
            # For safety, if it does not ends with the directory separator, we append it
            # to its end.
            directory += PyFunceble.directory_separator

        # We initiate a variable which will save the list of file to delete.
        result = []

        for root, _, files in PyFunceble.walk(directory):
            # We walk in the directory and get all files and sub-directories.

            for file in files:
                # If there is files in the current sub-directory, we loop
                # through the list of files.

                if file not in [".gitignore", ".keep"]:
                    # The file is not into our list of file we do not have to delete.

                    if root.endswith(PyFunceble.directory_separator):
                        # The root ends with the directory separator.

                        # We construct the path and append the full path to the result.
                        result.append(root + file)
                    else:
                        # The root directory does not ends with the directory separator.

                        # We construct the path by appending the directory separator
                        # between the root and the filename and append the full path to
                        # the result.
                        result.append(
                            root + PyFunceble.directory_separator + file
                        )  # pragma: no cover

        # We return our list of file to delete.
        return result

    @classmethod
    def databases_to_delete(cls):  # pragma: no cover
        """
        Set the databases files to delete.
        """

        # We initiate the directory we have to look for.
        directory = PyFunceble.CONFIG_DIRECTORY

        # We initate the result variable.
        result = []

        # We append the dir_structure file.
        result.append(
            "{0}{1}".format(
                directory,
                PyFunceble.CONFIGURATION["outputs"]["default_files"]["dir_structure"],
            )
        )

        # We append the iana file.
        result.append(
            "{0}{1}".format(
                directory, PyFunceble.CONFIGURATION["outputs"]["default_files"]["iana"]
            )
        )

        # We append the public suffix file.
        result.append(
            "{0}{1}".format(
                directory,
                PyFunceble.CONFIGURATION["outputs"]["default_files"]["public_suffix"],
            )
        )

        # We append the inactive database file.
        result.append(
            "{0}{1}".format(
                directory,
                PyFunceble.CONFIGURATION["outputs"]["default_files"]["inactive_db"],
            )
        )

        # We append the mining database file.
        result.append(
            "{0}{1}".format(
                directory,
                PyFunceble.CONFIGURATION["outputs"]["default_files"]["mining"],
            )
        )

        # We append the whois database file.
        result.append(
            "{0}{1}".format(
                directory,
                PyFunceble.CONFIGURATION["outputs"]["default_files"]["whois_db"],
            )
        )

        return result

    def almost_everything(self, clean_all=False):
        """
        Delete almost all discovered files.

        :param bool clean_all:
            Tell the subsystem if we have to clean everything instesd
            of almost everything.
        """

        # We get the list of file to delete.
        to_delete = self.file_to_delete()

        if clean_all:  # pragma: no cover
            to_delete.extend(self.databases_to_delete())

        for file in to_delete:
            # We loop through the list of file to delete.

            # And we delete the currently read file.
            File(file).delete()

        if clean_all:  # pragma: no cover
            PyFunceble.Load(PyFunceble.CONFIG_DIRECTORY)
