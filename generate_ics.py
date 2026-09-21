#!/usr/bin/env python3
"""Generate .ics calendars (Apple Calendar + Google Calendar) for MOGA Essaouira 2026.

Run:  python3 generate_ics.py
Output goes to ./calendars/. Edit the data below and re-run to regenerate;
UIDs are stable, so re-importing updates existing events instead of duplicating them.
"""
from datetime import datetime, timedelta, timezone
from pathlib import Path

TZID = "Africa/Casablanca"  # Morocco is UTC+1 in October (no Ramadan shift)
OUT = Path(__file__).parent / "calendars"
REMINDER = "-PT30M"  # 30 minutes before each set / party
BASE_URL = "https://hthoussam.github.io/moga-2026-calendar"
SITE_TITLE = "MOGA Essaouira 2026 · planner"
DISCLAIMER = ("Unofficial fan-made calendar. Venues, map pins and set times were taken from posters and the "
              "festival website and may be inaccurate or change — double-check with the official MOGA channels before you head out. "
              "Use at your own risk.")

FESTIVAL_VENUE = "Hôtel Le Golf d'Essaouira & Spa (ex-Sofitel Mogador), Essaouira, Morocco"
FESTIVAL_GEO = (31.470125, -9.7672651)
FESTIVAL_MAP = "https://maps.google.com/?q=31.470125,-9.7672651"
TICKETS = "https://www.mogafestival.com/tickets?event=essaouira"

STAGE_NOTES = {
    "Hafla": "",
    "Sqala": "",
    "J'rda": "",
    "Maalma": "Maalma stage curated by Supervibe.",
}

# Main festival timetable (from the official line-up-by-stage posters).
# Times are local; anything before 12:00 belongs to the next calendar day.
FESTIVAL = {
    "2026-10-02": {
        "label": "Friday 2 Oct",
        "Hafla": [
            ("16:00", "18:00", "Mov."),
            ("18:00", "19:30", "Florentia"),
            ("19:30", "21:30", "Othman Kabbadj"),
            ("21:30", "00:00", "Gawdat"),
            ("00:00", "02:00", "Jamie Jones"),
            ("02:00", "04:00", "Richy Ahmed"),
        ],
        "Sqala": [  # Cartoon Record showcase
            ("16:00", "18:00", "Asmun"),
            ("18:00", "20:00", "N4BZ"),
            ("20:00", "22:00", "Hamadeus"),
            ("22:00", "00:00", "Oz & Rem"),
            ("00:00", "02:00", "Jhobei"),
            ("02:00", "04:00", "Julian Anthony"),
        ],
        "J'rda": [
            ("16:00", "18:00", "Jilali"),
            ("18:00", "20:00", "Jakaw"),
            ("20:00", "00:00", "Piiticu"),
            ("00:00", "04:00", "Rhadoo"),
        ],
        "Maalma": [
            ("16:00", "18:00", "Oufras"),
            ("18:00", "20:00", "Waillis"),
            ("20:00", "22:00", "Yassir"),
            ("22:00", "00:00", "Rikku"),
            ("00:00", "02:00", "Tripple Seven"),
            ("02:00", "04:00", "De La Roza"),
        ],
    },
    "2026-10-03": {
        "label": "Saturday 3 Oct",
        "Hafla": [
            ("16:00", "18:00", "Jazzee & Meyzz"),
            ("18:00", "20:00", "Halfpint"),
            ("20:00", "22:00", "Jesse Calosso"),
            ("22:00", "00:00", "Matisa"),
            ("00:00", "02:00", "The Martinez Brothers"),
            ("02:00", "04:00", "Silvie Loto"),
        ],
        "Sqala": [
            ("16:00", "19:00", "Baruck b2b Mambaskar"),
            ("19:00", "21:00", "Abel"),
            ("21:00", "23:00", "Yamagucci"),
            ("23:00", "00:30", "Notre Dame"),
            ("00:30", "02:00", "Ramyen"),
            ("02:00", "04:00", "Notre Dame b2b Ramyen b2b Yamagucci"),
        ],
        "J'rda": [
            ("16:00", "18:00", "Hyde b2b Rain"),
            ("18:00", "21:00", "Mumsfilibaba"),
            ("21:00", "23:00", "Sonja Moonear"),
            ("23:00", "02:00", "Fantastic Man b2b Tornado Wallace"),
            ("02:00", "04:00", "Malika b2b Yaya (MA)"),
        ],
        "Maalma": [
            ("16:00", "18:00", "Acid Ramen"),
            ("18:00", "20:00", "Moruki"),
            ("20:00", "22:00", "Memed Awad"),
            ("22:00", "00:00", "Alexis Cabrera (Live)"),
            ("00:00", "02:00", "Calabasa"),
            ("02:00", "04:00", "Voigtmann"),
        ],
    },
    "2026-10-04": {
        "label": "Sunday 4 Oct",
        "Hafla": [
            ("16:00", "18:00", "Ebba"),
            ("18:00", "20:00", "Polyswitch"),
            ("20:00", "22:00", "Doudou MD"),
            ("22:00", "00:00", "Bradley Zero"),
            ("00:00", "02:00", "ANOTR"),
            ("02:00", "04:00", "Amine K b2b Daox"),
        ],
        "Sqala": [
            ("16:00", "19:00", "Loewenthal"),
            ("19:00", "21:30", "Kalabrese"),
            ("21:30", "00:00", "Viken Arman"),
            ("00:00", "02:00", "Fort Romeau"),
            ("02:00", "04:00", "Cesar Merveille"),
        ],
        "J'rda": [
            ("16:00", "19:00", "Ousseki"),
            ("19:00", "21:00", "Yahya (Live)"),
            ("21:00", "23:00", "DJ Senc"),
            ("23:00", "01:00", "Enrica Falqui"),
            ("01:00", "04:00", "Tunik"),
        ],
        "Maalma": [
            ("16:00", "18:00", "Umaedo"),
            ("18:00", "20:00", "Badr Ake"),
            ("20:00", "22:00", "Aykat"),
            ("22:00", "00:00", "Saul"),
            ("00:00", "02:00", "Ignacio Morales"),
            ("02:00", "04:00", "Ruven Medici"),
        ],
    },
}

# MOGA OFF parties. No individual set times are published, so each party is one
# event (reminder fires 30 min before doors) with the full line-up in the notes.
# (date, start, end, title, venue, geo, map_url, lineup, extra_url, key)
OFF_BEYTT = [
    ("2026-09-30", "19:00", "03:00", "MOGA OFF · Cartoon Record × Beytt Mogador",
     "Beytt Mogador, Essaouira", (31.5039488, -9.7632255),
     "https://maps.google.com/?q=31.5039488,-9.7632255",
     ["DJ Gamba", "Asmun", "Rem", "Oz", "Krimo"], "", "beytt"),
    ("2026-10-01", "19:00", "03:00", "MOGA OFF · Cartoon Record × Beytt Mogador",
     "Beytt Mogador, Essaouira", (31.5039488, -9.7632255),
     "https://maps.google.com/?q=31.5039488,-9.7632255",
     ["James Andrew (Live)", "Anirr", "N4BZ", "Sue", "Koko & Sanji"], "", "beytt"),
]

OFF_OTHER = [
    # Wednesday 30 Sep
    ("2026-09-30", "12:00", "19:00", "MOGA OFF · Pool Party at La Perle (Le Comptoir Electronik Taghazout)",
     "La Perle de Mogador Hotel, Essaouira", (31.4954804, -9.7569085),
     "https://maps.google.com/?q=31.4954804,-9.7569085",
     ["Alpha", "Felix ID", "Ivan Escura", "Rita Soko"], "", "laperle"),
    ("2026-09-30", "13:00", "01:30", "MOGA OFF · Megaloft",
     "Megaloft, Essaouira", (31.5132541, -9.7694854),
     "https://maps.google.com/?q=31.5132541,-9.7694854",
     ["Axis", "Boogiechalz", "DJ Alasa", "L82DP", "MKLF", "Mouta", "Rabbi", "Sparta", "SYC Gull", "Vikii"], "", "megaloft"),
    ("2026-09-30", "16:00", "02:00", "MOGA OFF · Taros (Apéros Electros)",
     "Taros, Essaouira", None,
     "https://www.google.com/maps/place//data=!4m2!3m1!1s0xdad9a4e9f588ccf:0x65843d760f3f7eb3",
     ["Bel Âge", "Benabdadil", "DJ Steaw", "Joe Lewandowski", "Nicola Moreno", "Souki", "Valentine Groove"], "", "taros"),
    ("2026-09-30", "17:00", "23:00", "MOGA OFF · Live Music at Sqala (Opening Concert) — free w/ RSVP",
     "Sqala, Essaouira medina", None, "https://maps.app.goo.gl/5DpsptY7JEzdhYuY7",
     ["Mask Off", "MOGA Academy DJs", "Mr ID", "Robin M", "Smemo"],
     "https://shotgun.live/fr/festivals/live-music-at-sqala-30-09", "sqala-live"),
    ("2026-09-30", "17:00", "01:30", "MOGA OFF · Le Palazzo (Reload)",
     "Hôtel Le Palazzo, Essaouira", (31.5113488, -9.7707799),
     "https://maps.google.com/?q=31.5113488,-9.7707799",
     ["Ayman", "Charlie", "Mikolaï", "Norman"], "", "palazzo"),
    ("2026-09-30", "18:00", "02:00", "MOGA OFF · Beach & Friends × Le Matin Records",
     "Beach & Friends, Essaouira", (31.4973091, -9.7630615),
     "https://maps.google.com/?q=31.4973091,-9.7630615",
     ["Anas M", "Otto", "Luca Ruiz", "Thomas Schmitt"], "", "beachfriends"),
    ("2026-09-30", "19:00", "01:30", "MOGA OFF · La Coupole (Shift Collective)",
     "La Coupole, Essaouira Beach", (31.5050081, -9.7635198),
     "https://maps.google.com/?q=31.5050081,-9.7635198",
     ["Azir", "Benaïssa", "Eden Azuelos", "Izi"], "", "coupole"),
    ("2026-09-30", "21:00", "02:00", "MOGA OFF · Cosmo",
     "Cosmo Mogador, Essaouira", (31.5121952, -9.7720978),
     "https://maps.google.com/?q=31.5121952,-9.7720978",
     ["Anthony Cox", "Soufwax", "Wolff"], "", "cosmo"),
    # Thursday 1 Oct
    ("2026-10-01", "12:00", "19:00", "MOGA OFF · Pool Party at La Perle (Le Comptoir Electronik Taghazout)",
     "La Perle de Mogador Hotel, Essaouira", (31.4954804, -9.7569085),
     "https://maps.google.com/?q=31.4954804,-9.7569085",
     ["Blackout", "Diego Knows", "Foxy From Space", "Yaya Alen"], "", "laperle"),
    ("2026-10-01", "13:30", "01:30", "MOGA OFF · Megaloft (REF)",
     "Megaloft, Essaouira", (31.5132541, -9.7694854),
     "https://maps.google.com/?q=31.5132541,-9.7694854",
     ["Andy Book", "Ayyu", "DJ Alasa", "Lüna", "Rabbi", "Sparta"], "", "megaloft"),
    ("2026-10-01", "16:00", "02:00", "MOGA OFF · Taros (Apéros Electros)",
     "Taros, Essaouira", None,
     "https://www.google.com/maps/place//data=!4m2!3m1!1s0xdad9a4e9f588ccf:0x65843d760f3f7eb3",
     ["Benabdadil", "Chinau", "Coleeeette", "Dymos", "Jamie 3:26", "Jay Fase", "Shizzo", "This is Yab"], "", "taros"),
    ("2026-10-01", "17:00", "23:00", "MOGA OFF · Live Music at Sqala — free w/ RSVP",
     "Sqala, Essaouira medina", None, "https://maps.app.goo.gl/5DpsptY7JEzdhYuY7",
     ["Billi", "Retro Cassetta", "Glitter55", "MOGA Academy DJs", "Monile"],
     "https://shotgun.live/fr/festivals/live-music-at-sqala-01-10", "sqala-live"),
    ("2026-10-01", "17:00", "01:30", "MOGA OFF · Le Palazzo (Reload)",
     "Hôtel Le Palazzo, Essaouira", (31.5113488, -9.7707799),
     "https://maps.google.com/?q=31.5113488,-9.7707799",
     ["CAP", "Holly Molly", "Topper"], "", "palazzo"),
    ("2026-10-01", "17:30", "02:30", "MOGA OFF · Villa Nour (Secte)",
     "Villa Nour, km 7 Douar El Ghazoua, Essaouira", (31.4547196, -9.7457477),
     "https://maps.google.com/?q=31.4547196,-9.7457477",
     ["Ashi", "Biisse", "E-Youb", "Julien Blanch", "Ladagnous", "Nico Rodas", "UU'B"], "", "villanour"),
    ("2026-10-01", "18:00", "02:00", "MOGA OFF · Beach & Friends × Le Matin Records",
     "Beach & Friends, Essaouira", (31.4973091, -9.7630615),
     "https://maps.google.com/?q=31.4973091,-9.7630615",
     ["Gabriel Belabbas", "Illspleen", "Mendy"], "", "beachfriends"),
    ("2026-10-01", "19:00", "01:30", "MOGA OFF · La Coupole (Shift Collective)",
     "La Coupole, Essaouira Beach", (31.5050081, -9.7635198),
     "https://maps.google.com/?q=31.5050081,-9.7635198",
     ["ANOIR", "Thomas & Steewa", "Tino", "Wailis"], "", "coupole"),
    ("2026-10-01", "21:00", "02:00", "MOGA OFF · Cosmo",
     "Cosmo Mogador, Essaouira", (31.5121952, -9.7720978),
     "https://maps.google.com/?q=31.5121952,-9.7720978",
     ["Anthony Cox", "DJ Donut", "Soufwax", "Victori1"], "", "cosmo"),
]

# ---------------------------------------------------------------------------

DTSTAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def esc(text):
    return text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold(line):
    """Fold at 75 octets per RFC 5545 (continuation lines start with a space)."""
    data = line.encode("utf-8")
    if len(data) <= 75:
        return line
    out, cur = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        limit = 75 if not out else 74
        if len(cur) + len(b) > limit:
            out.append(cur)
            cur = b
        else:
            cur += b
    out.append(cur)
    return "\r\n ".join(p.decode("utf-8") for p in out)


def local(date, hhmm, after_start=None):
    d = datetime.strptime(f"{date} {hhmm}", "%Y-%m-%d %H:%M")
    if after_start is not None and d <= after_start:
        d += timedelta(days=1)
    return d


def fmt(d):
    return d.strftime("%Y%m%dT%H%M%S")


def event(uid, summary, start, end, location, description, geo=None, url=None, categories=(), **meta):
    return dict(uid=uid, summary=summary, start=start, end=end, location=location,
                description=description, geo=geo, url=url, categories=categories, **meta)


def vevent(ev):
    lines = [
        "BEGIN:VEVENT",
        f"UID:{ev['uid']}",
        f"DTSTAMP:{DTSTAMP}",
        f"DTSTART;TZID={TZID}:{fmt(ev['start'])}",
        f"DTEND;TZID={TZID}:{fmt(ev['end'])}",
        f"SUMMARY:{esc(ev['summary'])}",
        f"LOCATION:{esc(ev['location'])}",
        f"DESCRIPTION:{esc(ev['description'])}",
    ]
    if ev["categories"]:
        lines.append("CATEGORIES:" + ",".join(esc(c) for c in ev["categories"]))
    if ev["url"]:
        lines.append(f"URL:{ev['url']}")
    if ev["geo"]:
        lat, lon = ev["geo"]
        lines.append(f"GEO:{lat};{lon}")
        lines.append(
            f'X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-RADIUS=300;X-TITLE="{ev["location"]}":geo:{lat},{lon}'
        )
    lines += [
        "BEGIN:VALARM",
        "ACTION:DISPLAY",
        f"DESCRIPTION:{esc(ev['summary'])} starts in 30 minutes",
        f"TRIGGER:{REMINDER}",
        "END:VALARM",
        "END:VEVENT",
    ]
    return lines


def festival_events(stages=None):
    events = []
    for date, day in FESTIVAL.items():
        day_start = local(date, "12:00")
        for stage, slots in day.items():
            if stage == "label" or (stages and stage not in stages):
                continue
            for s, e, artist in slots:
                start = local(date, s, day_start)
                end = local(date, e, start)
                notes = [
                    f"MOGA Essaouira 2026 — {day['label']}",
                    f"Stage: {stage}",
                    f"Set: {s}–{e}",
                ]
                if stage == "Sqala" and date == "2026-10-02":
                    notes.append("Cartoon Record showcase.")
                if STAGE_NOTES.get(stage):
                    notes.append(STAGE_NOTES[stage])
                notes += ["", f"Map: {FESTIVAL_MAP}", f"Tickets: {TICKETS}", "", DISCLAIMER]
                slug = stage.lower().replace("'", "")
                uid = f"moga2026-{date}-{slug}-{s.replace(':', '')}@moga-planning"
                events.append(event(
                    uid, f"{artist} · {stage}", start, end, FESTIVAL_VENUE,
                    "\n".join(notes), geo=FESTIVAL_GEO, url=TICKETS,
                    categories=("MOGA 2026", "MOGA", stage),
                    day=date, stage=stage, artist=artist, s=s, e=e,
                ))
    return events


def off_events(parties):
    events = []
    for date, s, e, title, venue, geo, map_url, lineup, extra, key in parties:
        start = local(date, s)
        end = local(date, e, start)
        notes = [
            f"MOGA OFF — {start.strftime('%A %-d %b')}",
            f"Doors: {s}–{e}",
            "Line-up: " + " · ".join(lineup),
            "(Individual set times not published — reminder is for doors.)",
            "",
            f"Map: {map_url}",
        ]
        if extra:
            notes.append(f"RSVP / info: {extra}")
        notes += ["", DISCLAIMER]
        uid = f"moga2026-off-{date}-{key}@moga-planning"
        events.append(event(
            uid, title, start, end, venue, "\n".join(notes), geo=geo,
            url=extra or map_url, categories=("MOGA 2026", "MOGA OFF"),
            day=date, stage="OFF", artist=title.replace("MOGA OFF · ", ""), s=s, e=e,
            lineup=lineup, map_url=map_url, extra=extra,
        ))
    return events


CAL_HEADER = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//moga-planning//MOGA Essaouira 2026//EN",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
]
VTIMEZONE = [
    "BEGIN:VTIMEZONE",
    f"TZID:{TZID}",
    "BEGIN:STANDARD",
    "DTSTART:20180101T000000",
    "TZOFFSETFROM:+0100",
    "TZOFFSETTO:+0100",
    "TZNAME:+01",
    "END:STANDARD",
    "END:VTIMEZONE",
]


def write_ics(path, calname, events):
    lines = CAL_HEADER + [f"X-WR-CALNAME:{esc(calname)}", f"X-WR-TIMEZONE:{TZID}"] + VTIMEZONE
    for ev in events:
        lines += vevent(ev)
    lines.append("END:VCALENDAR")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\r\n".join(fold(l) for l in lines) + "\r\n", encoding="utf-8")


def write_calendar(name, calname, events):
    write_ics(OUT / f"{name}.ics", calname, events)
    print(f"{name + '.ics':45} {len(events):3} events")


# --------------------------------------------------------------------------- landing page

from html import escape as h
from urllib.parse import quote, urlencode


def gcal_template_url(ev):
    q = urlencode({
        "action": "TEMPLATE",
        "text": ev["summary"],
        "dates": f"{fmt(ev['start'])}/{fmt(ev['end'])}",
        "ctz": TZID,
        "location": ev["location"],
        "details": ev["description"],
    }, quote_via=quote)
    return "https://calendar.google.com/calendar/render?" + q


def event_file(ev):
    return f"calendars/events/{ev['uid'].split('@')[0]}.ics"


def cal_links(rel_path, label):
    """Subscribe/add/download links for one .ics file."""
    if BASE_URL:
        abs_url = f"{BASE_URL}/{rel_path}"
        apple = "webcal://" + abs_url.split("://", 1)[1]
        google = "https://calendar.google.com/calendar/r?cid=" + quote(abs_url, safe="")
    else:  # local preview only
        apple, google = rel_path, rel_path
    return (
        f'<a class="btn apple" href="{h(apple)}">🍎 Apple / iPhone</a>'
        f'<a class="btn google" href="{h(google)}" target="_blank" rel="noopener">📅 Google Calendar</a>'
        f'<a class="btn file" href="{h(rel_path)}" download>⬇️ .ics file</a>'
    )


def write_index(all_events, fest, off_beytt, off_other):
    days = {}
    for ev in all_events:
        days.setdefault(ev["day"], []).append(ev)
    day_names = {
        "2026-09-30": "Wed 30 Sep · MOGA OFF",
        "2026-10-01": "Thu 1 Oct · MOGA OFF",
        "2026-10-02": "Fri 2 Oct",
        "2026-10-03": "Sat 3 Oct",
        "2026-10-04": "Sun 4 Oct",
    }
    stages = ("Hafla", "Sqala", "J'rda", "Maalma")

    def set_row(ev):
        add = f'<a href="{h(gcal_template_url(ev))}" target="_blank" rel="noopener" title="Add to Google Calendar">G</a>'
        add += f'<a href="{h(event_file(ev))}" title="Add to Apple Calendar">🍎</a>'
        return (f'<li><span class="t">{ev["s"]}–{ev["e"]}</span>'
                f'<span class="a">{h(ev["artist"])}</span><span class="add">{add}</span></li>')

    def off_row(ev):
        add = f'<a href="{h(gcal_template_url(ev))}" target="_blank" rel="noopener" title="Add to Google Calendar">G</a>'
        add += f'<a href="{h(event_file(ev))}" title="Add to Apple Calendar">🍎</a>'
        rsvp = f' · <a href="{h(ev["extra"])}" target="_blank" rel="noopener">RSVP</a>' if ev["extra"] else ""
        return (f'<li class="off"><div><span class="t">{ev["s"]}–{ev["e"]}</span>'
                f'<span class="a">{h(ev["artist"])}</span><span class="add">{add}</span></div>'
                f'<div class="meta">📍 <a href="{h(ev["map_url"])}" target="_blank" rel="noopener">{h(ev["location"])}</a>{rsvp}</div>'
                f'<div class="meta">{h(" · ".join(ev["lineup"]))}</div></li>')

    sections = []
    for date in ("2026-09-30", "2026-10-01"):
        rows = "".join(off_row(ev) for ev in sorted(days[date], key=lambda x: x["start"]))
        sections.append(f'<section class="day"><h2>{day_names[date]}</h2><ul class="sets">{rows}</ul></section>')
    for date in ("2026-10-02", "2026-10-03", "2026-10-04"):
        cols = []
        for st in stages:
            rows = "".join(set_row(ev) for ev in days[date] if ev["stage"] == st)
            cols.append(f'<div class="stage"><h3>{h(st)}</h3><ul class="sets">{rows}</ul></div>')
        sections.append(f'<section class="day"><h2>{day_names[date]} · 16:00–04:00</h2><div class="stages">{"".join(cols)}</div></section>')

    pick = [
        ("MOGA-2026-OFF-Beytt-Cartoon.ics", "OFF · Cartoon Record × Beytt Mogador (30 Sep, 1 Oct)"),
        ("MOGA-2026-OFF-other-parties.ics", "OFF · all other parties (30 Sep, 1 Oct)"),
        ("MOGA-2026-Festival-all-stages.ics", "Festival · all 4 stages (2–4 Oct)"),
        ("MOGA-2026-Festival-Hafla.ics", "Festival · Hafla stage only"),
        ("MOGA-2026-Festival-Sqala.ics", "Festival · Sqala stage only"),
        ("MOGA-2026-Festival-Jrda.ics", "Festival · J'rda stage only"),
        ("MOGA-2026-Festival-Maalma.ics", "Festival · Maalma stage only"),
    ]
    pick_html = "".join(
        f'<li><span>{h(label)}</span><span class="links">{cal_links("calendars/" + f, label)}</span></li>'
        for f, label in pick
    )

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{h(SITE_TITLE)}</title>
<style>
:root{{--blue:#1747d6;--ink:#0e1a4a;--cream:#fbf5dd;--card:#fffdf4;--muted:#5b6285}}
*{{box-sizing:border-box}}
body{{margin:0;font:16px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--blue);color:var(--ink);padding:16px 16px 48px}}
main{{max-width:1080px;margin:0 auto}}
header{{color:#fff;text-align:center;padding:24px 0 8px}}
header h1{{font-size:clamp(34px,7vw,56px);margin:0;letter-spacing:.02em;line-height:1}}
header p{{margin:8px 0 0;opacity:.9}}
.card{{background:var(--cream);border-radius:18px;padding:20px;margin:18px 0}}
.card h2{{margin:0 0 6px;font-size:22px}}
.hero .btns{{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}}
.btn{{display:inline-block;padding:12px 16px;border-radius:12px;font-weight:600;text-decoration:none;color:#fff;background:var(--ink)}}
.btn.apple{{background:#111}} .btn.google{{background:#1a73e8}} .btn.file{{background:#4a5590}}
.hero .btn{{font-size:17px;flex:1 1 200px;text-align:center}}
.note{{font-size:14px;color:var(--muted);margin:10px 0 0}}
details{{margin-top:12px}} summary{{cursor:pointer;font-weight:600}}
ul.pick{{list-style:none;padding:0;margin:8px 0 0}}
ul.pick li{{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px;padding:10px 0;border-top:1px solid #e6dfbf}}
ul.pick .links{{display:flex;flex-wrap:wrap;gap:6px}} ul.pick .btn{{padding:6px 10px;font-size:13px;border-radius:8px}}
.day{{margin-top:22px}} .day h2{{color:#fff;font-size:24px;margin:0 0 10px}}
.stages{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}}
.stage{{background:var(--card);border-radius:14px;padding:12px 14px}}
.stage h3{{margin:0 0 6px;font-size:18px;text-transform:uppercase;letter-spacing:.06em;color:var(--blue)}}
ul.sets{{list-style:none;margin:0;padding:0}}
ul.sets li{{display:flex;align-items:center;gap:8px;padding:7px 0;border-top:1px solid #efe8c8}}
ul.sets li:first-child{{border-top:0}}
.t{{font-variant-numeric:tabular-nums;color:var(--muted);font-size:13px;min-width:88px}}
.a{{font-weight:700;flex:1}}
.add a{{display:inline-block;margin-left:4px;padding:2px 7px;border-radius:6px;background:#e9e3c4;color:var(--ink);text-decoration:none;font-size:12px;font-weight:700}}
li.off{{display:block;background:var(--card);border-radius:14px;padding:10px 14px;margin-bottom:8px;border:0}}
li.off>div{{display:flex;align-items:center;gap:8px}} .meta{{font-size:13px;color:var(--muted);margin-top:4px;display:block}}
.meta a{{color:var(--blue)}}
.disclaimer{{background:#fff3c4;color:#5a3d00;border:1px solid #f0c94a;border-radius:12px;padding:10px 14px;font-size:14px;margin:14px 0 0}}
footer{{color:#fff;opacity:.8;font-size:13px;text-align:center;margin-top:30px}} footer a{{color:#fff}}
</style></head><body><main>
<header><h1>MOGA ESSAOUIRA 26</h1><p>30 Sep – 4 Oct 2026 · Hôtel Le Golf d'Essaouira &amp; Spa (ex-Sofitel Mogador) · times are Essaouira local (UTC+1)</p></header>

<p class="disclaimer">⚠️ {h(DISCLAIMER)}</p>

<div class="card hero">
<h2>Add everything to your calendar</h2>
<p class="note" style="margin-top:0">All {len(all_events)} events: both OFF nights + every DJ set on all 4 stages, each with a reminder 30 min before.</p>
<div class="btns">{cal_links("calendars/MOGA-2026-ALL.ics", "everything")}</div>
<p class="note"><b>iPhone / Mac:</b> tap Apple → <i>Subscribe</i>. On Mac, untick "Remove alerts" in the subscribe dialog so the 30-min reminders stay.<br>
<b>Google:</b> tap Google → <i>Add calendar</i>. Google ignores reminders on subscribed calendars, so once: Settings → the “MOGA Essaouira 2026” calendar → <i>Event notifications</i> → add <b>30 minutes</b>. (Or import the .ics file instead — imports keep the reminders.)</p>
<details><summary>Only want part of it? Pick a calendar</summary><ul class="pick">{pick_html}</ul></details>
</div>

{"".join(sections)}

<footer>Buttons next to each set add just that one: <b>G</b> = Google Calendar, 🍎 = Apple. OFF parties don't publish set times, so the reminder is for doors.<br>
<a href="https://mogafestival.com/" target="_blank" rel="noopener">mogafestival.com</a> · <a href="{h(TICKETS)}" target="_blank" rel="noopener">tickets</a> · Sqala on Friday = Cartoon Record showcase · Maalma stage by Supervibe</footer>
</main></body></html>
"""
    (Path(__file__).parent / "index.html").write_text(page, encoding="utf-8")
    print(f"{'index.html':45} {len(all_events):3} events")


if __name__ == "__main__":
    beytt = off_events(OFF_BEYTT)
    other = off_events(OFF_OTHER)
    fest = festival_events()
    everything = beytt + other + fest

    write_calendar("MOGA-2026-ALL", "MOGA Essaouira 2026", everything)
    write_calendar("MOGA-2026-OFF-Beytt-Cartoon", "MOGA OFF · Beytt × Cartoon", beytt)
    write_calendar("MOGA-2026-OFF-other-parties", "MOGA OFF · other parties", other)
    write_calendar("MOGA-2026-Festival-all-stages", "MOGA 2026 · all stages", fest)
    for stage in ("Hafla", "Sqala", "J'rda", "Maalma"):
        slug = stage.replace("'", "")
        write_calendar(f"MOGA-2026-Festival-{slug}", f"MOGA 2026 · {stage}", festival_events({stage}))
    for ev in everything:  # one-event files for the per-set Apple buttons
        write_ics(Path(__file__).parent / event_file(ev), ev["summary"], [ev])
    write_index(everything, fest, beytt, other)
