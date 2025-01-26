<template>
    <button class = "download" :style = "{ 'background-color': selected.cdb != '' ? 'cornflowerblue' : 'gray' }" @click = "() => { emitter.emit('event_save_before_download'); } ">保存</button>
</template>

<script setup name="download" lang="js">
    import { ref, reactive, watch, onMounted, computed } from 'vue';
    import axios from 'axios';
    import emitter from '@/utils/emitter';

    let selected = reactive({
        cdb: ''
    });

    emitter.on('event_select_or_leave_cdb', (cdb = '') => {
        selected.cdb = cdb;
    });

    emitter.on('event_save_over', download_cdb);

    async function download_cdb(cdb) {
        try {
            let response = await axios.post('http://127.0.0.1:8000/api/download_cdb', {
                cdb: cdb
            }, { responseType: 'blob' });

            let blob = new Blob([response.data], { type: 'application/octet-stream' });
            let opts = {
                suggestedName: `${cdb.replace('.cdb', '')}.ypk`,
                types: [{
                    description: '',
                    accept: {
                        'application/octet-stream': ['.ypk']
                    }
                }],
                excludeAcceptAllOption: true
            };

            let handle = await window.showSaveFilePicker(opts);
            let writable = await handle.createWritable();
            await writable.write(blob);
            await writable.close();

        } catch (error) {}
    }
</script>
