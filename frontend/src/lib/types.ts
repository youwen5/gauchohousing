export type ApartmentEntry = {
  name: string
  address: string
  description?: string
  phoneNumber?: string
  priceRange?: PriceRange
  thumbnail?: string
  beds?: string
}

type PriceRange = [number, number]
