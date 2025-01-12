import type { PageLoad } from './$types'
import GeoJSON from 'geojson'

export const load: PageLoad = async ({ fetch }) => {
  try {
    const data = await fetch('http://localhost:8000/get-all-apartments')
    const { apartments } = await data.json()

    const crimeData = await fetch('http://localhost:8000/get-all-crime')
    const crime = await crimeData.json()

    interface Crime {
      id: number
      crime_name: string
      latitude: number
      longitude: number
      relevant_to_party_map: boolean
    }

    // If your input data is wrapped in an object like:
    // { crimes: Crime[] }
    interface CrimesData {
      crimes: Crime[]
    }

    // 1. Partition crimes into two arrays
    function partitionCrimes(crimes: Crime[]) {
      const relevantCrimes = crimes.filter((crime) => crime.relevant_to_party_map)
      const nonRelevantCrimes = crimes.filter((crime) => !crime.relevant_to_party_map)

      return { relevantCrimes, nonRelevantCrimes }
    }

    // 2. Convert an array of Crime objects into a GeoJSON FeatureCollection
    function createGeoJSON(crimes: Crime[]): GeoJSON.FeatureCollection {
      return {
        type: 'FeatureCollection',
        features: crimes.map((crime) => {
          return {
            type: 'Feature',
            properties: {
              // You can leave this empty if desired:
              // properties: {}
              // Or store some fields, e.g.:
              crime_name: crime.crime_name,
              id: crime.id
            },
            geometry: {
              type: 'Point',
              // Use [longitude, latitude, elevation]
              // If elevation is unknown, default to 0 (sea level)
              coordinates: [crime.longitude, crime.latitude, 0]
            }
          }
        })
      }
    }

    const { relevantCrimes, nonRelevantCrimes } = partitionCrimes(crime.crimes)

    const relevantGeoJSON = createGeoJSON(relevantCrimes)
    const nonRelevantGeoJSON = createGeoJSON(nonRelevantCrimes)

    return { apartments, partyCrime: relevantGeoJSON, otherCrime: nonRelevantGeoJSON }
  } catch (err) {
    return { apartments: null }
  }
}
