export type ApartmentEntry = {
  name: string
  address: string
  longitude: number
  latitude: number
  description?: string
  phoneNumber?: string
  priceRange?: PriceRange
  thumbnail?: string
  beds?: string
}

type PriceRange = [number, number]
