<script lang="ts">
  import * as Popover from '$lib/components/ui/popover'
  import * as Table from '$lib/components/ui/table'
  import { Rating } from 'flowbite-svelte'
  import Badges from './badges.svelte'
  import { HouseIcon, PlusCircle } from 'lucide-svelte/icons'
  import type { ApartmentEntry } from '$lib/types'
  import { apartmentStore } from "$lib/store"
  import { Button } from '$lib/components/ui/button/index.js'

  const { price, name, address, thumbnail, rating, phone, beds} = $props()

  function addHouse(price: string, the_name:string, address:string, thumbnail:string, phone:string, beds:string){

      let minPrice: number = 0;
      let maxPrice: number = 0;

      if(price)
      {
        const [minPriceString, maxPriceString] = price.split("-");
        minPrice = parseInt(minPriceString?.replace("$", ""), 10); // Use parseInt for whole numbers
        maxPrice = parseInt(maxPriceString?.replace("$", ""), 10); // Use parseFloat for potential decimals
      }

      const apartment_store: ApartmentEntry = {
        name: the_name,
        address: address,
        description: "I like this House",
        phoneNumber: phone,
        priceRange: [minPrice,maxPrice],
        thumbnail: thumbnail,
        beds: beds
      }

      let temp = $apartmentStore
      temp.push(apartment_store)  

      apartmentStore.set(temp)
    }

</script>

<Popover.Root>
  <Popover.Trigger>
    <HouseIcon class="scale-75 hover:scale-100 transition-all" />
  </Popover.Trigger>
  <Popover.Content class="sm:w-[600px] rounded-2xl">
    <div class="border-accent rounded-lg p-4 border-2 overflow-y-auto max-h-[50vh]">
      <span class="text-xl font-bold">{name}</span>
      <div class="flex flex-row justify-between">
        <div class="block">
          <Rating class="-ml-1 mt-1" id="apartment-rating" total={5} size={35} {rating} />
          <Badges />
        </div>
        <Button variant="ghost" onclick={() => addHouse(price, name, address, thumbnail,phone,beds)}>
          <PlusCircle class="scale-150"/>
        </Button>
      </div>
      <img src={thumbnail} alt={name} class="rounded-lg drop-shadow-xl mt-4 max-w-[100%]" />
      <p class="my-4">
        {address}
      </p>

      <Table.Root>
        <Table.Caption>Information</Table.Caption>
        <Table.Header>
          <Table.Row>
            <Table.Head>Price</Table.Head>
            <Table.Head>Beds</Table.Head> 
            <Table.Head>Phone Number</Table.Head>
          </Table.Row>
        </Table.Header>
        <Table.Body>
            <Table.Row>
              <Table.Cell class="font-medium">{price}</Table.Cell>
              <Table.Cell>{beds}</Table.Cell>
              <Table.Cell>{phone}</Table.Cell>
            </Table.Row>
        </Table.Body>
      </Table.Root>
    </div>
  </Popover.Content>
</Popover.Root>
