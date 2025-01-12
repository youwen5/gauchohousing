<script lang="ts">
  import { buttonVariants } from '$lib/components/ui/button/index.js'
  import { Input } from '$lib/components/ui/input/index.js'
  import { Label } from '$lib/components/ui/label/index.js'
  import * as Popover from '$lib/components/ui/popover/index.js'
  import { Cog } from 'lucide-svelte/icons'
  import Switch from './ui/switch/switch.svelte'
  import { settingsStore } from '$lib/store'
</script>

<Popover.Root>
  <Popover.Trigger class={buttonVariants({ variant: 'outline' })}>
    <span class="flex items-center gap-2">
      <Cog />
      Map Settings
    </span>
  </Popover.Trigger>
  <Popover.Content class="w-60">
    <div class="grid gap-4">
      <div class="space-y-2">
        <h4 class="font-medium leading-none">Map Settings</h4>
        <p class="text-muted-foreground text-sm">Configure visual artifacts in the map.</p>
      </div>
      <div class="grid gap-2">
        <div class="grid grid-cols-3 items-center gap-4">
          <Label for="width" class="col-span-2">Party heatmap</Label>
          <Switch bind:checked={$settingsStore.showParties} />
        </div>
        <div class="grid grid-cols-3 items-center gap-4">
          <Label for="width" class="col-span-2">Crime heatmap</Label>
          <Switch bind:checked={$settingsStore.showCrimes} />
        </div>
      </div>
    </div>
  </Popover.Content>
</Popover.Root>
