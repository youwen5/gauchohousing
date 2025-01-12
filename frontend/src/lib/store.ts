import { writable } from 'svelte/store'
import type { ApartmentEntry } from '$lib/types'

export const apartmentStore = writable<Array<ApartmentEntry>>([])

type Settings = {
  showParties: boolean
  showCrimes: boolean
}

export const settingsStore = writable<Settings>({
  showParties: true,
  showCrimes: true
})

