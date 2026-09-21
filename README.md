# MOGA Essaouira 2026 — calendar files

**Share this link:** https://hthoussam.github.io/moga-2026-calendar/
(one page with "Add everything" buttons for Apple/iPhone and Google Calendar, the full timetable, and a per-set add button)

Direct subscribe URLs (everything, auto-updates if the lineup changes):
- Apple / iPhone: `webcal://hthoussam.github.io/moga-2026-calendar/calendars/MOGA-2026-ALL.ics`
- Google: https://calendar.google.com/calendar/r?cid=https%3A%2F%2Fhthoussam.github.io%2Fmoga-2026-calendar%2Fcalendars%2FMOGA-2026-ALL.ics

To update: edit `generate_ics.py`, run `python3 generate_ics.py`, commit and push — subscribers get the changes automatically.

`.ics` files work in both **Apple Calendar** and **Google Calendar**. Every event has a **30‑minute reminder**.
All times are Essaouira local time (Africa/Casablanca, UTC+1).

## Files (`calendars/`)

| File | What's in it |
|---|---|
| `MOGA-2026-ALL.ics` | Everything below in one go (86 events) |
| `MOGA-2026-OFF-Beytt-Cartoon.ics` | MOGA OFF · Cartoon Record × Beytt Mogador — 30 Sep & 1 Oct (19:00–03:00) |
| `MOGA-2026-OFF-other-parties.ics` | All other MOGA OFF parties from the official program (Megaloft, Taros, La Coupole, Cosmo, Palazzo, Beach & Friends, Villa Nour, La Perle pool party, Sqala live music) |
| `MOGA-2026-Festival-all-stages.ics` | Main festival, 2–4 Oct, every DJ set on all 4 stages (67 sets) |
| `MOGA-2026-Festival-Hafla.ics` / `-Sqala.ics` / `-Jrda.ics` / `-Maalma.ics` | One stage only — handy if you want to follow a single stage |

Main venue: Hôtel Le Golf d'Essaouira & Spa (ex‑Sofitel Mogador) — 1 venue, 4 stages (Hafla, Sqala, J'rda, Maalma).
Event titles are `Artist · Stage`, e.g. `Jamie Jones · Hafla`.

## Import — Apple Calendar

- **Mac:** double‑click the `.ics` → pick "New Calendar" (it will be named e.g. "MOGA Essaouira 2026") → OK.
- **iPhone/iPad:** AirDrop / WhatsApp / email the `.ics` to yourself → tap it → **Add All** → choose the calendar.

## Import — Google Calendar

1. On desktop: calendar.google.com → ⚙️ **Settings** → **Import & export**.
2. (Recommended) first create a new calendar called "MOGA 2026" (left sidebar → **+** next to *Other calendars* → *Create new calendar*).
3. **Select file from your computer** → choose the `.ics` → pick the "MOGA 2026" calendar → **Import**.
4. Share that calendar with friends (Settings → the calendar → *Share with specific people*), or just send them the `.ics`.

## Notes

- ⚠️ **Disclaimer:** unofficial, fan-made. Venues, map pins and set times come from posters and the festival website and may be inaccurate or change — check the official MOGA channels before heading out. Use at your own risk.

- OFF parties don't publish individual set times, so each party is one event with the full line‑up in the notes; the reminder fires 30 min before doors.
- Friday's Sqala stage is the Cartoon Record showcase; the Maalma stage is curated by Supervibe.
- To change anything, edit `generate_ics.py` and run `python3 generate_ics.py`. UIDs are stable, so re‑importing updates events instead of duplicating them.
