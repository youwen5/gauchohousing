# GauchoHousing

Submission for SB Hacks XI, UC Santa Barbara's annual hackathon. We ended up
winning 1st place in [Aryn](https://www.aryn.ai/)'s prize category.

Our team consisted of:

- [Youwen (Me)](https://youwen.dev)
- [Matthew](https://github.com/ANYhackerfort)
- [Tony](https://github.com/TonyL221)
- [Kevin](https://github.com/Makkerel)

Our stack was [Svelte](https://svelte.dev/) and SvelteKit alongside a
Selenium/[Sycamore](https://github.com/aryn-ai/sycamore) powered web scraper
and data ingester. The harvested data was served a REST API on a Django
webserver.

We also made heavy use of the Google Maps API for geocoding as well as
OpenStreetView data.

## Hacking

This project consists of both a SvelteKit full stack component in `frontend`
and a Django server in `backend` that performs the data harvesting.

To run it, you need the `pnpm` package manager for Node, and `nodejs` itself.
You also need the `uv` package manager for Python, but you don't need to
install python (`uv`) provides it.

Once you have the prerequisite tools, do the following

### Place the API keys in the right places

You need an API key from MapBuilder and an API key from the Google Maps API
(obtained in the Google Cloud Console). You need to place these within `.env` files in `frontend` and `backend`.

Inside of `frontend`, provide the MapBuilder API key:

Contents of `frontend/.env`:

```
PUBLIC_MAPTILER_KEY=YOUR_KEY_HERE
```

Then provide the Google Maps API key to the backend:

Contents of `backend/.env`:

```
MAPS_API_KEY=DONT_LEAK_UR_KEY
```

Once you've put these keys in the right place, you can start. It is possible
that the backend will run without the Google Maps API key, however it will not
be able to do any new Geocoding.


### Start the backend

`cd` into `backend`, then run:

```sh
uv run manage.py runserver
```

Dependencies and Python will be provided automagically. This will start the Django server at `localhost:8000`.

### Start the frontend

You must start the backend first. Then `cd` into `frontend`. Run

```sh
pnpm install
pnpm run dev
```

This will create the development server at `localhost:5173`. If all goes well,
you should see the site!

## Inspiration

It's common knowledge that UCSB has a housing crisis and many students stress over finding housing every year. We wanted to create a platform that would accomplish the following goals:

1. Streamline the process of finding student housing by aggregating multiple sources of information into just one place
2. Help students make more informed decisions about their housing choice

Our key distinction from other aggregation sites like Apartments.com or Redfin
is that we specifically scrape data tailored to the UCSB and greater IV
community. We wanted to also show things like listings on the UCSB subreddit or
lesser known local companies that aren't included in these large corporate-run
sites. We value automation over toil, so we focused on creating a streamlined process to quickly process virtually any housing or forum sites into structured data.

When using sites like Apartments.com, they are rarely the "last stop" for any
student researching housing, because there's so many other local options they
don't list. Our goal was to highlight these local options and make them more
accessible to the community.

## What it does

We built a website that takes in listings from many different sources,
including individual websites, places like `apartments.com`, and forums of
students looking for subletters and the like, and then places them all on one
map where students can browse around their options in IV. They can add their
favorite choices to a shopping cart that saves them until it's time to review.

We also provide a heatmap that shows areas where violent crimes occurred in the
past year, as well as a heatmap of partying in the past year, to help students
make more informed choices.

## How we built it

Our project consists of two equally important components. First, the actual
user facing website that has an interactive map and informational widgets for
the user to interact with and click. We built this using the Svelte UI
framework, on top of the SvelteKit full-stack framework that provides goodies
like server side rendering and server functions. The map is provided by
OpenStreetView, and implemented with a thin Svelte wrapper on the
maplibre-openGL project.

Second, we built a semi-automated data ingestion pipeline powered by Aryn (Sycamore) and Claude AIs. Aryn's AI was instrumental in our implementation, we entirely rely on it to convert the unstructured websites of housing companies and forums into well-formed data we can programmatically use.

Our data harvesting flow looks something like this: we first use Selenium, an automated browser driver, to visit websites and obtain text and screenshots. We run screenshots and other
artifacts we discover such as PDFs through Aryn to receive structured data that
we can insert into our database. Claude is used to perform a basic sanity check
on the data, such as ensuring formatting is correct and it's properly
structured. We don't generate anything new with Claude, and all of the actual
information comes from Aryn's parsing.

We insert our verified data into a database, and then use the Google Maps
Geocoding APIs to convert the addresses parsed by Aryn into actual coordinates
we can plot on a map. We then store all of this information back in the
database, which is powered by a Django web server that also implements a REST
API that our frontend uses for data access.

The violent crime heatmap comes from official data released by the UCPD. The partying heatmap is extrapolated from the location of possession of alcohol charges as well as noise ordinance violations.

## Challenges we ran into

At first, we were simply trying to download the raw HTML of websites in order
to parse them with Aryn. We quickly found that this doesn't work for many
complex websites that require JavaScript to run. We decided to spin up a
Selenium webdriver that can access sites like a human and obtain data for Aryn.

## Accomplishments that we're proud of

We're very proud of the general UX the map provides. We obtained 3D data from
MapBuilder to generate the 3D overlay of buildings on the map. In general the
map graphics such as heatmaps and popovers look quite polished for a hack.

## What we learned

It was most of our team member's first time using the Svelte and SvelteKit
frameworks as well as working with a real-world production-style web app. We
wrote our own APIs and server-side code, something most of us haven't done
before.

Also, we realized it is very important when designing full stack apps to design
and build the frontend to run on mock data, so that development isn't
bottlenecked by progress on the backend.

Most of us also learned the value of package managers like uv, scoop, and pnpm as a way to quickly download and manage the many dependencies required for both the backend and the frontend of the project. 
