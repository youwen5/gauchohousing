<script lang="ts">
  import {
    MapLibre,
    FillExtrusionLayer,
    Marker,
    GeoJSON,
    CircleLayer,
    HeatmapLayer,
    NavigationControl,
    GeolocateControl
  } from 'svelte-maplibre'
  import { writable } from 'svelte/store'
  import { PUBLIC_MAPTILER_KEY } from '$env/static/public'
  import MapPopover from '$lib/components/map-popover.svelte'
  import { onMount } from 'svelte'
  import type { PageData } from './$types'
  import { settingsStore } from '$lib/store'

  let { data }: { data: PageData } = $props()
  let { apartments, partyCrime, otherCrime } = data

  let clickedName = writable('')
  const bounds = [-119.890895, 34.395773, -119.828927, 34.442636] as [
    number,
    number,
    number,
    number
  ] // [minLng, minLat, maxLng, maxLat]

  const streetsStyle = `https://api.maptiler.com/maps/streets-v2/style.json?key=${PUBLIC_MAPTILER_KEY}`

  onMount(() => {
    console.log(apartments)
    console.log(otherCrime)
    console.log(partyCrime)
  })
</script>

{#if data}
  <main class="fixed inset-0 h-screen w-screen z-0">
    <MapLibre
      style={streetsStyle}
      class="absolute inset-0"
      center={[-119.856801, 34.413044]}
      zoom={14.8}
      maxBounds={bounds}
      filterLayers={(l) => l.id !== 'building-3d'}
    >
      <NavigationControl visualizePitch={true} position="top-right" />
      <GeolocateControl position="top-right" fitBoundsOptions={{ maxZoom: 12 }} />
      {#each apartments as { latitude, longitude, apartment_name, price_range, address, bedroom_types, phone_number, image_link }}
        <Marker
          lngLat={[longitude, latitude]}
          onclick={() => clickedName.set(apartment_name)}
          class="grid h-8 w-8 place-items-center rounded-full border border-gray-200 bg-red-300 text-black shadow-2xl focus:outline-2 focus:outline-black"
        >
          <MapPopover
            name={apartment_name}
            {address}
            price={price_range}
            beds={bedroom_types}
            phone={phone_number}
            thumbnail={image_link}
            rating={4.5}
          />
        </Marker>
      {/each}

      <FillExtrusionLayer
        source="maptiler_planet"
        sourceLayer="building"
        beforeLayerType={(l) => l.type === 'symbol' && !!l.paint?.['text-color']}
        minzoom={14}
        paint={{
          'fill-extrusion-color': [
            'interpolate',
            ['linear'],
            ['get', 'render_height'],
            0,
            '#0a0',
            70,
            '#a00'
          ],
          'fill-extrusion-height': [
            'interpolate',
            ['linear'],
            ['zoom'],
            14,
            0,
            14.05,
            ['get', 'render_height']
          ],
          'fill-extrusion-base': [
            'interpolate',
            ['linear'],
            ['zoom'],
            14,
            0,
            14.05,
            ['get', 'render_min_height']
          ],
          'fill-extrusion-opacity': 0.6
        }}
      />
      {#if $settingsStore.showParties}
        <GeoJSON id="parties" data={partyCrime}>
          <HeatmapLayer
            minzoom={14.2}
            paint={{
              // 1. Make sure the weight doesn't go to zero
              'heatmap-weight': [
                'interpolate',
                ['linear'],
                ['get', 'mag'],
                0,
                0.5, // Even at mag=0, assign some weight (0.5)
                2,
                1 // If mag=2 is a typical high
              ],

              // 2. Increase intensity so hotspots are more obvious
              'heatmap-intensity': [
                'interpolate',
                ['linear'],
                ['zoom'],
                0,
                1,
                9,
                4 // More intense at high zoom
              ],

              // 3. Increase radius so points cover larger areas (especially at lower zoom)
              'heatmap-radius': [
                'interpolate',
                ['linear'],
                ['zoom'],
                0,
                10, // Start bigger than 2
                9,
                40 // End bigger than 20
              ],

              // 4. Keep the layer from vanishing at zoom >= 9
              'heatmap-opacity': [
                'interpolate',
                ['linear'],
                ['zoom'],
                7,
                1,
                14,
                0.4 // No fadeout
              ],

              // 5. Adjust color ramp as you see fit
              'heatmap-color': [
                'interpolate',
                ['linear'],
                ['heatmap-density'],
                0,
                'rgba(33,102,172,0)',
                0.2,
                '#0CAFFF',
                0.4,
                '#89CFF0',
                0.6,
                '#6CB4EE',
                0.8,
                '#007FFF',
                1,
                '#0CAFFF'
              ]
            }}
          />

          <CircleLayer
            id="parties"
            source="parties"
            maxzoom={14.2}
            paint={{
              // Size circle radius by earthquake magnitude and zoom level
              'circle-radius': [
                'interpolate',
                ['linear'],
                ['zoom'],
                7,
                ['interpolate', ['linear'], ['get', 'mag'], 1, 1, 6, 4],
                16,
                ['interpolate', ['linear'], ['get', 'mag'], 1, 5, 6, 50]
              ],
              // Color circle by earthquake magnitude
              'circle-color': [
                'interpolate',
                ['linear'],
                ['get', 'mag'],
                1,
                'rgba(33,102,172,0)',
                2,
                'rgb(103,169,207)',
                3,
                'rgb(209,229,240)',
                4,
                'rgb(253,219,199)',
                5,
                'rgb(239,138,98)',
                6,
                'rgb(178,24,43)'
              ],
              'circle-stroke-color': 'white',
              'circle-stroke-width': 1,
              // Transition from heatmap to circle layer by zoom level
              'circle-opacity': ['interpolate', ['linear'], ['zoom'], 7, 0, 8, 1]
            }}
          />
        </GeoJSON>
      {/if}
      {#if $settingsStore.showCrimes}
        <GeoJSON id="crimes" data={otherCrime}>
          <HeatmapLayer
            minzoom={14.2}
            paint={{
              // 1. Make sure the weight doesn't go to zero
              'heatmap-weight': [
                'interpolate',
                ['linear'],
                ['get', 'mag'],
                0,
                0.5, // Even at mag=0, assign some weight (0.5)
                2,
                1 // If mag=2 is a typical high
              ],

              // 2. Increase intensity so hotspots are more obvious
              'heatmap-intensity': [
                'interpolate',
                ['linear'],
                ['zoom'],
                0,
                1,
                9,
                4 // More intense at high zoom
              ],

              // 3. Increase radius so points cover larger areas (especially at lower zoom)
              'heatmap-radius': [
                'interpolate',
                ['linear'],
                ['zoom'],
                0,
                10, // Start bigger than 2
                9,
                40 // End bigger than 20
              ],

              // 4. Keep the layer from vanishing at zoom >= 9
              'heatmap-opacity': [
                'interpolate',
                ['linear'],
                ['zoom'],
                7,
                1,
                14,
                0.3 // No fadeout
              ],

              // 5. Adjust color ramp as you see fit
              'heatmap-color': [
                'interpolate',
                ['linear'],
                ['heatmap-density'],
                0,
                'rgba(33,102,172,0)',
                0.2,
                'rgb(103,169,207)',
                0.4,
                'rgb(209,229,240)',
                0.6,
                'rgb(253,219,199)',
                0.8,
                'rgb(239,138,98)',
                1,
                'rgb(178,24,43)'
              ]
            }}
          />

          <CircleLayer
            id="crimes"
            source="crimes"
            maxzoom={14.2}
            paint={{
              // Size circle radius by earthquake magnitude and zoom level
              'circle-radius': [
                'interpolate',
                ['linear'],
                ['zoom'],
                7,
                ['interpolate', ['linear'], ['get', 'mag'], 1, 1, 6, 4],
                16,
                ['interpolate', ['linear'], ['get', 'mag'], 1, 5, 6, 50]
              ],
              // Color circle by earthquake magnitude
              'circle-color': [
                'interpolate',
                ['linear'],
                ['get', 'mag'],
                1,
                'rgba(33,102,172,0)',
                2,
                'rgb(103,169,207)',
                3,
                'rgb(209,229,240)',
                4,
                'rgb(253,219,199)',
                5,
                'rgb(239,138,98)',
                6,
                'rgb(178,24,43)'
              ],
              'circle-stroke-color': 'white',
              'circle-stroke-width': 1,
              // Transition from heatmap to circle layer by zoom level
              'circle-opacity': ['interpolate', ['linear'], ['zoom'], 7, 0, 8, 1]
            }}
          />
        </GeoJSON>
      {/if}
    </MapLibre>
  </main>
{:else}
  <h1>Backend is not running and/or configured properly!</h1>
{/if}
