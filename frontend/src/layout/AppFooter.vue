<script setup>
import { useLayout } from '@/layout/composables/layout';
import { computed } from 'vue';

const { layoutConfig } = useLayout();

const logoUrl = computed(() => {
    return `/layout/images/${layoutConfig.darkTheme.value ? 'logo-white' : 'logo-dark'}.svg`;
});
</script>

<template>
    <div class="layout-footer">
        <div class="flex justify-center">
            <span class="text-xs text-slate-400">Created By: Cyril Seberiaga </span>
            <span class="text-xs text-slate-400">© 2024 Guimaras Provincial Government</span>
        </div>
    </div>
</template>
<style lang="scss" scoped></style>
