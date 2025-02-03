<template>
    <el-button class = "download" @click = "emit.card_page.save.to()">
        <el-icon><Download/></el-icon>
        <span>下载</span>
    </el-button>
</template>

<script setup name="download" lang="js">
    import { ref, reactive, watch, onMounted, computed } from 'vue';
    import axios from 'axios';
    import emitter from '@/utils/emitter';

    let open = reactive({
        cdb: ''
    });

    let emit = {
        card_page : {
            save : {
                to : function() {
                    emitter.emit('to_cpage_save');
                },
                on : function() {
                    download_cdb();
                }
            },
            cdb_opened : {
                on : function(cdb) {
                    open.cdb = cdb[0][0];
                }
            },
            cdb_closed : {
                on : function() {
                    open.cdb = '';
                }
            }
        }
    }

    emitter.on('to_cpage_cdb_closed', emit.card_page.cdb_closed.on);
    emitter.on('to_cpage_cdb_opened', emit.card_page.cdb_opened.on);
    emitter.on('to_dpage_save', emit.card_page.save.on);

    async function download_cdb() {
        try {
            let response = await axios.post(`${window.location.href}api/download_cdb`, {
                cdb: open.cdb
            }, { responseType: 'blob' });

            let blob = new Blob([response.data], { type: 'application/octet-stream' });
            let opts = {
                suggestedName: `${open.cdb.replace('.cdb', '')}.ypk`,
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
