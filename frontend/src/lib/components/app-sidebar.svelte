<script lang="ts">
  import * as Sidebar from '$lib/components/ui/sidebar/index.js'
  import * as Card from '$lib/components/ui/card/index.js'
  import { Map, House, SparkleIcon, ArrowBigLeft, Trash } from 'lucide-svelte/icons'

  import Button from './ui/button/button.svelte'
  import Settings from '$lib/components/settings.svelte'
  import Slide from '$lib/components/price-slider.svelte'
  import type { ApartmentEntry } from '$lib/types'
  import { apartmentStore } from '$lib/store'
  import { fly } from 'svelte/transition'

  let activeSelection = $state('main')
  function changeSelection(focus: string) {
    activeSelection = focus
  }

  const items = [
    {
      title: 'Saved Housing',
      icon: House
    },
    {
      title: 'Recommended',
      icon: SparkleIcon
    }
  ]

  function deleteHouse(index: number) {
    let temp = $apartmentStore
    temp.splice(index, 1)

    apartmentStore.set(temp)
  }
</script>

{#if activeSelection === 'main'}
  <Sidebar.Root class="m-4 border-2 rounded-lg border-accent shadow-2xl max-h-[95%]">
    <Sidebar.Content class="p-4">
      <Sidebar.Group>
        <Sidebar.GroupLabel class="text-5xl font-bold text-foreground mb-4"
          >GauchoHome</Sidebar.GroupLabel
        >
        <Sidebar.GroupContent class="bg-transparent border-none mt-8">
          <Sidebar.Menu>
            {#each items as item (item.title)}
              <Sidebar.MenuItem>
                <Sidebar.MenuButton>
                  {#snippet child({ props })}
                    <button {...props} onclick={() => changeSelection(item.title)}>
                      <item.icon />
                      <span class="text-2xl">{item.title}</span>
                    </button>
                  {/snippet}
                </Sidebar.MenuButton>
              </Sidebar.MenuItem>
            {/each}
          </Sidebar.Menu>
        </Sidebar.GroupContent>
      </Sidebar.Group>
      <Slide />
    </Sidebar.Content>
    <Sidebar.Footer>
      <Settings />
    </Sidebar.Footer>
  </Sidebar.Root>
{/if}

{#if activeSelection === 'Saved Housing'}
  <Sidebar.Root class="m-4 border-2 rounded-lg border-accent shadow-2xl max-h-[95%]">
    <Sidebar.Header class="flex flex-row items-center text-center text-xl font-bold">
      <Button variant="outline" size="icon" onclick={() => changeSelection('main')}>
        <ArrowBigLeft />
      </Button>
      <div>Saved Housing</div>
    </Sidebar.Header>
    <Sidebar.Content>
      <Sidebar.Group>
        <Sidebar.Menu>
          {#each $apartmentStore as house, i (house)}
            <div transition:fly={{ x: -20 }}>
              <Sidebar.MenuItem
                class="transition justify-items-center border-2 border-transparent border-solid hover:border-current"
              >
                <img class="object-fill" src={house.thumbnail} alt="house" />
                <Card.Root class="rounded-none w-[100%]">
                  <Card.Header>
                    <Card.Title>
                      {house.name}
                    </Card.Title>
                    <Card.Description>
                      <p>{@html house.address}</p>
                      <p><b>Price:</b> ${house.priceRange?.[0]} - ${house.priceRange?.[1]}</p>
                    </Card.Description>
                  </Card.Header>
                  <Card.Content>
                    <p>{@html house.description}</p>
                    <p>{@html house.beds}</p>
                  </Card.Content>
                  <Card.Footer>
                    Call: {house.phoneNumber}
                  </Card.Footer>
                </Card.Root>

                <Sidebar.MenuAction
                  onclick={() => deleteHouse(i)}
                  class="px-4 py-2 rounded-xl bg-red-500 shadow-lg"
                >
                  <Trash />
                </Sidebar.MenuAction>
              </Sidebar.MenuItem>
            </div>
          {/each}
        </Sidebar.Menu>
      </Sidebar.Group>
    </Sidebar.Content>
    <Sidebar.Footer>
      <Button>Calculate Homeless Index</Button>
    </Sidebar.Footer>
  </Sidebar.Root>
{/if}

{#if activeSelection === 'Recommended'}
  <Sidebar.Root class="m-4 border-2 rounded-lg border-accent shadow-2xl max-h-[95%]">
    <Sidebar.Header class="flex flex-row items-center text-center text-xl font-bold">
      <Button variant="outline" size="icon" onclick={() => changeSelection('main')}>
        <ArrowBigLeft />
      </Button>
      <div>Recommend me</div>
    </Sidebar.Header>
    <Sidebar.Content></Sidebar.Content>
    <Sidebar.Footer>
      <Button>Claude AI + Our Own Agent</Button>
    </Sidebar.Footer>
  </Sidebar.Root>
{/if}
