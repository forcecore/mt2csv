#!/usr/bin/env python

import sys
import pandas as pd


class Mt2csv:
    def __init__(self):
        self.df = None
        self.simulator = ""
        self.title = ""

    def yield_tokens(self, f):
        for line in f:
            for tok in line.split():
                yield tok

    def read_header(self, tokens):
        """
        tokens: iterator that yields tokens. (Must not be a list!)
        """
        header = []
        for tok in tokens:
            header.append(tok)
            if tok.find('#') >= 0:
                break
        return header

    def yield_rows(self, tokens, header_len):
        # If you have .alter in spice, you get multiple measurements.
        # In other words, you get multiple rows.
        # optimize.mt0 is an example of this case.
        row = []
        for tok in tokens:
            row.append(float(tok))
            if len(row) >= header_len:
                yield row
                row = []
        assert len(row) == 0, "Left-over data detected"

    def parse_tokens(self, f):
        """
        Updates self.data.
        f: stream object
        """
        tokens = self.yield_tokens(f)
        header = self.read_header(tokens)
        df = pd.DataFrame(columns=header,
                          data=self.yield_rows(tokens, len(header)))
        return df

    def read(self, fname):
        with open(fname) as f:
            self.simulator = f.readline().strip()
            self.title = f.readline().strip()
            self.df = self.parse_tokens(f)

    def to_csv(self, f):
        """
        f: stream, str, path object or anything that works with df.to_csv()
        """
        print(self.simulator)
        print(self.title)
        self.df.to_csv(f)


###
### main
###
if __name__ == "__main__":
    fname = sys.argv[1]
    ofname = sys.argv[2]
    mt2csv = Mt2csv()
    mt2csv.read(fname)
    mt2csv.to_csv(ofname)
    print("Wrote", ofname)
