from dataclasses import dataclass
import datetime as dt
from pathlib import Path


@dataclass
class IcsReturn:
    title: str
    path: Path
    dt_start: dt.datetime
    dt_end: dt.datetime
    url: str


SUMMARY1 = "SUMMARY;LANGUAGE=en-US:"
SUMMARY2 = "SUMMARY;LANGUAGE=pt-BR:"
DTSTART = "DTSTART;TZID"
DTEND = "DTEND;TZID"
DTFMT = "%Y%m%dT%H%M%S"
TIMEZONE1 = "E. South America Standard Time"
TIMEZONE2 = "America/Sao_Paulo"
URL = "X-MICROSOFT-SKYPETEAMSMEETINGURL:"


def parse_dt_start(path: Path) -> IcsReturn:
    title = ""
    dt_start: dt.datetime | None = None
    dt_end: dt.datetime | None = None
    with path.open() as ics:
        while line := next(ics):
            if line.startswith(SUMMARY1):
                title = line.removeprefix(SUMMARY1).strip()
            elif line.startswith(SUMMARY2):
                title = line.removeprefix(SUMMARY2).strip()
            if line.startswith(DTSTART):
                try:
                    dt_start = dt.datetime.strptime(line.strip(), f"{DTSTART}={TIMEZONE1}:{DTFMT}")
                except ValueError:
                    dt_start = dt.datetime.strptime(line.strip(), f"{DTSTART}={TIMEZONE2}:{DTFMT}")
            if line.startswith(DTEND):
                try:
                    dt_end = dt.datetime.strptime(line.strip(), f"{DTEND}={TIMEZONE1}:{DTFMT}")
                except ValueError:
                    dt_end = dt.datetime.strptime(line.strip(), f"{DTEND}={TIMEZONE2}:{DTFMT}")
            if line.startswith(URL):
                if title == "" or dt_start is None or dt_end is None:
                    raise ValueError(f"Could not find {SUMMARY1} or {SUMMARY2} or {DTSTART} or {DTEND} in {path}")
                link = line.removeprefix(URL).strip()
                while tmp := next(ics):
                    if tmp[0] == " ":
                        link += tmp.strip()
                    else:
                        break
                return IcsReturn(title, path, dt_start, dt_end, link)
    raise ValueError(f"Could not find {URL} in {path}")


def order_dt_start(entries: list[IcsReturn]) -> list[IcsReturn]:
    return sorted(entries, key=lambda entry: entry.dt_start)


def main(path: Path) -> None:
    meetings: list[IcsReturn] = []
    for entry in path.iterdir():
        if entry.is_dir():
            continue
        if entry.suffix == ".ics":
            meetings.append(parse_dt_start(entry))
    meetings = order_dt_start(meetings)
    for meet in meetings:
        print(f"{meet.dt_start:%Y/%m/%d %H:%M}~{meet.dt_end:%H:%M} > {str(meet.path):<15}")
        print(f"{' ' * 11}{meet.url} > {meet.title:<40}")


if __name__ == "__main__":
    main(Path())
