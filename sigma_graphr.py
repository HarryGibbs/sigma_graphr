import sys
import csv
import re
import os
import zipfile
import tempfile
import shutil


def parse_fas(file_path):
    headers = []
    seqs = []
    with open(file_path, 'r', encoding='utf-8', errors='replace', newline=None) as f:
        header = None
        seq = []
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith('>'):
                if header is not None:
                    headers.append(header)
                    seqs.append(''.join(seq))
                header = line[1:].strip()
                seq = []
            else:
                seq.append(line)
        if header is not None:
            headers.append(header)
            seqs.append(''.join(seq))

    if not headers:
        raise ValueError('no sequences parsed')

    return headers, seqs


def clean_name(name):
    n = re.sub(r'\s+', '_', name)
    n = re.sub(r'[^0-9A-Za-z_]+', '', n)
    n = n.strip('_') or 'sequence'
    return n


def dedupe_names(names):
    out = []
    seen = {}
    for n in names:
        c = seen.get(n, 0) + 1
        seen[n] = c
        out.append(n if c == 1 else f'{n}_{c}')
    return out


def write_csv(out_path, seq_name, seq):
    letters = sorted(set(seq))
    if not letters:
        return False

    with open(out_path, 'w', newline='', encoding='utf-8') as csvfile:
        w = csv.writer(csvfile, lineterminator='\n')
        w.writerow([seq_name + '_Position'] + letters)
        counts = {l: 0 for l in letters}
        for i, ch in enumerate(seq, 1):
            if ch in counts:
                counts[ch] += 1
            w.writerow([i] + [counts[l] for l in letters])

    return True


def process_one_file(file_path, outdir, base_prefix_single=False, zip_if_multi=False):
    headers, seqs = parse_fas(file_path)

    cleaned = [clean_name(h) for h in headers]
    names = dedupe_names(cleaned)

    base = os.path.splitext(os.path.basename(file_path))[0]
    base_clean = clean_name(base)

    if zip_if_multi and len(names) > 1:
        tmpdir = tempfile.mkdtemp(prefix='sigmagraphr_', dir=outdir)
        written_paths = []
        try:
            for name, seq in zip(names, seqs):
                out_path = os.path.join(tmpdir, f'{name}_sigmagraphr_output.csv')
                if write_csv(out_path, name, seq):
                    written_paths.append(out_path)

            if not written_paths:
                raise ValueError('no output generated')

            zip_path = os.path.join(outdir, f'{base_clean}_sigmagraphr_output.zip')
            with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
                for p in written_paths:
                    z.write(p, arcname=os.path.basename(p))

            return {'mode': 'zip', 'path': zip_path, 'count': len(written_paths)}
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    written = 0
    out_paths = []

    for name, seq in zip(names, seqs):
        if base_prefix_single:
            out_name = f'{base_clean}_{name}_sigmagraphr_output.csv'
        else:
            out_name = f'{name}_sigmagraphr_output.csv'

        out_path = os.path.join(outdir, out_name)
        if write_csv(out_path, name, seq):
            written += 1
            out_paths.append(out_path)

    if written == 0:
        raise ValueError('no output generated')

    return {'mode': 'csv', 'paths': out_paths, 'count': written}


def list_input_files(input_dir):
    exts = ('.fas', '.fasta', '.fa')
    files = []
    for f in os.listdir(input_dir):
        p = os.path.join(input_dir, f)
        if os.path.isfile(p) and f.lower().endswith(exts):
            files.append(p)
    return sorted(files)


def main():
    if len(sys.argv) >= 3:
        file_path = sys.argv[1]
        outdir = sys.argv[2]
        if not os.path.isfile(file_path):
            sys.stderr.write('input file not found\n')
            return 1
        os.makedirs(outdir, exist_ok=True)
        try:
            process_one_file(file_path, outdir, base_prefix_single=False, zip_if_multi=False)
        except Exception as e:
            sys.stderr.write(str(e) + '\n')
            return 1
        return 0

    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, 'input')
    outdir = os.path.join(base_dir, 'output')

    if not os.path.isdir(input_dir):
        sys.stderr.write('missing input folder: ' + input_dir + '\n')
        return 1

    os.makedirs(outdir, exist_ok=True)

    files = list_input_files(input_dir)
    if not files:
        sys.stderr.write('no .fas files found in input folder\n')
        return 1

    failed = 0
    for p in files:
        try:
            process_one_file(p, outdir, base_prefix_single=True, zip_if_multi=True)
        except Exception as e:
            failed += 1
            sys.stderr.write(os.path.basename(p) + ': ' + str(e) + '\n')

    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
