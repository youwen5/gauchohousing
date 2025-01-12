<script lang="ts">
  import { buttonVariants } from '$lib/components/ui/button/index.js'
  import { Input } from '$lib/components/ui/input/index.js'
  import { Label } from '$lib/components/ui/label/index.js'

  import * as Accordion from '$lib/components/ui/accordion'
  import { DollarSign } from 'lucide-svelte/icons'
  import { Slider } from '$lib/components/ui/slider/index.js'
  import { fly } from 'svelte/transition'

  // Initialize value as a reactive store
  let value = $state([1000, 3000])
</script>

<Accordion.Root type="single">
  <Accordion.Item value="prices" class="px-4">
    <Accordion.Trigger>
      <span class="inline-flex gap-2">
        <DollarSign class="text-xl" />
        Prices
      </span>
    </Accordion.Trigger>

    <Accordion.Content class="w-full max-w-md mx-auto p-4 mt-4 transition-transform">
      <div class="space-y-4">
        <h4 class="text-xl font-semibold">Set Price Range</h4>
        <p class="text-sm text-gray-600">Adjust the price range using the slider below:</p>

        <div class="space-y-6">
          <!-- Slider -->
          <div class="flex justify-center items-center gap-4">
            <Slider
              type="multiple"
              bind:value
              max={10000}
              min={100}
              step={100}
              class="w-[80%] h-2"
            />
          </div>

          <div class="slider-values flex justify-between text-lg font-medium text-gray-700">
            <span>{value[0]}</span>
            <span>{value[1]}</span>
          </div>

          <!-- Inputs for min and max price -->
          <div class="grid gap-4">
            <div class="grid grid-cols-3 items-center gap-4">
              <Label for="min_price" class="text-sm font-medium">Min Price</Label>
              <Input
                id="min_price"
                bind:value={value[0]}
                class="col-span-2 h-8 rounded-md border p-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition-colors"
              />
            </div>
            <div class="grid grid-cols-3 items-center gap-4">
              <Label for="max_price" class="text-sm font-medium">Max Price</Label>
              <Input
                id="max_price"
                bind:value={value[1]}
                class="col-span-2 h-8 rounded-md border p-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition-colors"
              />
            </div>
          </div>
        </div>
      </div>
    </Accordion.Content>
  </Accordion.Item>
</Accordion.Root>

<style>
  .slider-values {
    margin-top: 8px;
    font-weight: bold;
  }

  .slider-values span {
    width: 45%;
    text-align: center;
  }
</style>
