from urllib.request import urlopen
from numpy import loadtxt
from bs4 import BeautifulSoup
from datetime import datetime


inFileName = "table_SWIFT_no_MATCH_SDSS.txt"

positions = loadtxt(inFileName, comments="#", usecols=(1, 2), unpack=True)
positions = list(enumerate(zip(*positions)))
nPos = len(positions)

outFileName = "Swift_match.txt"
outFileHandler = open(outFileName, "w")

outFileHandler.write("# Swift match results\n")
outFileHandler.write("# * dataset           : dataset identifier\n")
outFileHandler.write("# * ra                : right ascension\n")
outFileHandler.write("# * dec               : declination\n")
outFileHandler.write("# * observation begin : begin observation time (UT)\n")
outFileHandler.write("# * observation end   : end observation time (UT)\n")
outFileHandler.write("# * band              : observation band\n")
outFileHandler.write("# * upper limit       : 3-σ upper limit [s^-1]\n")
outFileHandler.write("# * counts            : \n")
outFileHandler.write("# * background        : \n")
outFileHandler.write("# * corr fact         : \n")
outFileHandler.write("# * exposure          : [s] \n")
outFileHandler.write("# * main group        : Main dataset identifier used for compound observations\n")
outFileHandler.write("#\n")
outFileHandler.write("{0:>1s}".format("#"))
outFileHandler.write("{0:>11s}".format("dataset"))
outFileHandler.write("{0:>12s}".format("ra"))
outFileHandler.write("{0:>12s}".format("dec"))
outFileHandler.write("{0:>22s}".format("observation begin"))
outFileHandler.write("{0:>22s}".format("observation end"))
outFileHandler.write("{0:>12s}".format("band"))
outFileHandler.write("{0:>12s}".format("upper limit"))
outFileHandler.write("{0:>12s}".format("counts"))
outFileHandler.write("{0:>12s}".format("background"))
outFileHandler.write("{0:>12s}".format("corr fact"))
outFileHandler.write("{0:>12s}".format("exposure"))
outFileHandler.write("{0:>12s}".format("main group"))
outFileHandler.write("\n")

errFileName = "Swift_errors.txt"
errFileHandler = open(errFileName, "w")

errFileHandler.write("# List of cordinates with issues in parsing server response")
errFileHandler.write("\n")
errFileHandler.write("{0:>1s}".format("#"))
errFileHandler.write("{0:>11s}".format("ra"))
errFileHandler.write("{0:>12s}".format("dec"))

startTime = datetime.now()

for id, (ra, dec) in positions:
    progress = (id+1)*100.0/nPos

    data = {
        "searchpos": "{0:},{1:}".format(ra, dec),  # coordinates as pairs
        "forWhat": "1",  # 1: All datasets | 0: Deepest dataset
        "total": "on",  # "on" or None
        "soft": "on",  # "on" or None
        "medium": "on",  # "on" or None
        "hard": "on",  # "on" or None
    }

    dataStr = "&".join([
        "{0:}={1:}".format(k, v) for k, v in data.items() if v is not None
    ])

    dataStr = dataStr.encode("utf-8")

    url = "http://www.swift.ac.uk/1SXPS/processUL.php"

    request = urlopen(url, data=dataStr)

    textResponse = request.read()

    textResponse = textResponse.decode("utf-8").replace("</tr>\n</tr>", "</tr>")
    textResponse = textResponse.replace("</tr>\n</tr>", "</tr>")
    textResponse = textResponse.replace("</tr>\n</div>", "</tr></table></div>")

    parsedResponse = BeautifulSoup(textResponse, "html.parser")

    blocks = parsedResponse.findAll("div")

    for block in blocks:
        if block["id"] == "ResultDiv":
            resultContainer = block

            elapsedTime = datetime.now() - startTime

            print("")
            print("*** Progress    : {0:>.3f}%".format(progress))
            print("*** Elapsed Time: {0:}".format(elapsedTime))
            print("***", resultContainer.findAll("p")[0].getText())

            if resultContainer.findAll("table"):

                print("*** SUCCESS ***:", "Getting server response")
                for table in resultContainer.findAll("table"):
                    mainGroup = None

                    for row in table.findAll("tr"):
                        cols = row.findAll("td")
                        nCols = len(cols)

                        if nCols > 1:
                            error_pair = None
                            try:
                                if nCols == 7:
                                    SwiftRecord = {
                                        "ra": ra,
                                        "dec": dec,
                                        "dataset": None,
                                        "observation": {
                                            "begin": None,
                                            "end": None,
                                        },
                                        "band": None,
                                        "upper_limit": None,
                                        "counts": None,
                                        "background": None,
                                        "corr_fact": None,
                                        "exposure": None,
                                        "mainGroup": None,
                                    }

                                    for n, col in enumerate(cols):
                                        if n == 0:
                                            linkText = col.a.getText()
                                            ObservationDate = col.getText()
                                            ObservationDate = ObservationDate.replace(linkText, "")
                                            ObservationDate = ObservationDate.replace(" UT", "")
                                            ObservationDate = ObservationDate.replace("- ", "--")
                                            ObservationDate = ObservationDate.replace(" ", "T")
                                            ObservationDate = ObservationDate.replace("--", " ")

                                            SwiftRecord["dataset"] = col.a["href"].split("/")[-1]
                                            SwiftRecord["observation"]["begin"] = ObservationDate.split()[0]
                                            SwiftRecord["observation"]["end"] = ObservationDate.split()[1]
                                            SwiftRecord["mainGroup"] = mainGroup

                                            if mainGroup is None:
                                                SwiftRecord["mainGroup"] = "-"
                                                mainGroup = col.a["href"].split("/")[-1]

                                        elif n == 1:
                                            SwiftRecord["band"] = col.getText()
                                        elif n == 2:
                                            val, base, exp = [float(x) for x in col.getText().replace(" s-1", "").replace("&times", ";").split(";")]
                                            SwiftRecord["upper_limit"] = val * base ** exp
                                        elif n == 3:
                                            SwiftRecord["counts"] = col.getText()
                                        elif n == 4:
                                            SwiftRecord["background"] = col.getText()
                                        elif n == 5:
                                            SwiftRecord["corr_fact"] = col.getText()
                                        elif n == 6:
                                            SwiftRecord["exposure"] = col.getText().replace(" s", "")

                                elif nCols == 5:
                                    for n, col in enumerate(cols):
                                        if n == 0:
                                            SwiftRecord["band"] = col.getText()
                                        elif n == 1:
                                            val, base, exp = [float(x) for x in col.getText().replace(" s-1", "").replace("&times", ";").split(";")]
                                            SwiftRecord["upper_limit"] = val * base ** exp
                                        elif n == 2:
                                            SwiftRecord["counts"] = col.getText()
                                        elif n == 3:
                                            SwiftRecord["background"] = col.getText()
                                        elif n == 4:
                                            SwiftRecord["corr_fact"] = col.getText()

                                outFileHandler.write("{0:>12s}".format(SwiftRecord["dataset"]))
                                outFileHandler.write("{0:>12.6f}".format(SwiftRecord["ra"]))
                                outFileHandler.write("{0:>12.6f}".format(SwiftRecord["dec"]))
                                outFileHandler.write("{0:>22s}".format(SwiftRecord["observation"]["begin"]))
                                outFileHandler.write("{0:>22s}".format(SwiftRecord["observation"]["end"]))
                                outFileHandler.write("{0:>12s}".format(SwiftRecord["band"]))
                                outFileHandler.write("{0:>12.1e}".format(SwiftRecord["upper_limit"]))
                                outFileHandler.write("{0:>12s}".format(SwiftRecord["counts"]))
                                outFileHandler.write("{0:>12s}".format(SwiftRecord["background"]))
                                outFileHandler.write("{0:>12s}".format(SwiftRecord["corr_fact"]))
                                outFileHandler.write("{0:>12s}".format(SwiftRecord["exposure"]))
                                outFileHandler.write("{0:>12s}".format(SwiftRecord["mainGroup"]))
                                outFileHandler.write("\n")
                            except:
                                if error_pair != (ra, dec):
                                    error_pair = (ra, dec)
                                    errFileHandler.write("{0:>12.6f}".format(ra))
                                    errFileHandler.write("{0:>12.6f}".format(dec))
                                    errFileHandler.write("\n")
                                print("*** ERROR   ***:", "Parsing server response")

                            print("*** SUCCESS ***:", "Parsing and saving server response")

            else:
                print("*** ERROR   ***:", resultContainer.findAll("p")[1].getText())

outFileHandler.close()
