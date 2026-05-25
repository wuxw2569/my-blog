<script setup lang="ts">
import usePosts from '../../composables/usePosts'

const { allPosts: posts } = usePosts()
</script>

<template>
  <div class="grid gap-6 lg:grid-cols-2 mt-6">
    <div v-for="post of posts" :key="post">
      <Post :post="post" />
    </div>
  </div>
</template>
