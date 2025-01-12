<script lang="ts">
  import { Toaster } from 'svelte-sonner'
  import '../app.css'
  import * as Sidebar from '$lib/components/ui/sidebar/index.js'
  import AppSidebar from '$lib/components/app-sidebar.svelte'
  let { children } = $props()
</script>

<Toaster />

<Sidebar.Provider style="--sidebar-width: 25rem">
  <AppSidebar />
  <main>
    <!--<Sidebar.Trigger class="relative z-10" />-->
    {@render children?.()}
  </main>
</Sidebar.Provider>
