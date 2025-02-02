<template>
    <div class = "main_page">
        <div id = "main_page_left">
            <transition name = "slide_list_page">
                <list_page v-if = "main_page.show_list.card" @event_close_cdb = "main_page.remove" @event_unshow_list_page = "main_page.show" />
            </transition>
            <transition name = "under_list_page">
                <div v-if = "main_page.show_list.cdb" id = "under_list_page">
                    <div style = "display: flex; width: 30vw; height: 10vh;">
                        <div id = "add_area" @click = "main_page.add()"><h4>新建</h4></div>
                        <div id = "upload_area" @dragenter.prevent="main_page.uploading = true" @dragover.prevent="main_page.uploading = true" @dragleave.prevent="main_page.uploading = false" @drop.prevent="upload_file.drag" @click="() => { upload_file_input.click(); }">
                            <h4>拖拽文件或点击此处上传文件</h4>
                            <input type = "file" multiple accept="image/*, text/*, .lua, .cdb, .ypk, .zip, .tar, .tgz, .tar.gz, .7z, .rar" ref = "upload_file_input" @change = "upload_file.click" style = "display: none;"/>
                        </div>
                    </div>
                    <div id = "cdb_list">
                        <button v-for="(i, v) in (main_page.page.count > 0? Array(main_page.cdb.content.length >= main_page.page.count * 10? 10 : main_page.cdb.content.length % 10) : [])" :key="v" @click = "main_page.show(v)">{{ main_page.cdb.content[v + (Math.abs(main_page.page.count) - 1) * 10] }}</button>
                    </div>
                    <div class = "cdb_list_btn">
                        <button @click = "main_page.page.previous"
                            :style = "{ 'background-color': main_page.page.count <= 1 ? 'gray' : 'green', 'color': main_page.page.count <= 1 ? 'black' : 'white' }"
                        >上一页</button>
                        <span>第<input @input = "main_page.page.filter($event)" v-model = "main_page.page.count"/>页<br>共{{ Math.ceil(main_page.cdb.content.length / 10) }}页</span>
                        <button @click = "main_page.page.next"
                            :style = "{ 'background-color': main_page.page.count >= Math.ceil(main_page.cdb.content.length / 10) ? 'gray' : 'green', 'color': main_page.page.count >= Math.ceil(main_page.cdb.content.length / 10) ? 'black' : 'white' }"
                        >下一页</button>
                    </div>
                </div>
            </transition>
        </div>
        <card_page/>
    </div>
</template>

<script setup lang = "ts">
    import list_page from './components/list.vue'
    import card_page from './components/card.vue'

    import { ref, reactive, watch, onMounted, computed } from 'vue';
    import axios from 'axios';
    import emitter from '@/utils/emitter';

    let opening_cdb = ref('');

    let main_page = reactive({
        page : {
            count : 0,
            next : function () {
                if (main_page.page.count < Math.ceil(main_page.cdb.content.length / 10))
                    main_page.page.count ++ ;
            } as () => void,
            previous : function () {
                if (main_page.page.count > 1)
                    main_page.page.count -- ;
            } as () => void,
            filter : function (event) {
                let input_value = event.target.value;
                let new_value = input_value.replace(/[^0-9]/, '');
                while (parseInt(new_value) > Math.ceil(main_page.cdb.content.length / 10))
                    new_value = new_value.slice(0, -1);
                if (new_value == '')
                    new_value = 0;
                if (parseInt(new_value) < 1 && Math.ceil(main_page.cdb.content.length / 10) > 0)
                    new_value = 1;
                main_page.page.count = new_value;
            } as (event: any) => void
        },
        cdb : {
            content : [] as string[],
            get : async function (v) {
                let data = [[''], []];
                try {
                    let response = await axios.post('http://127.0.0.1:8000/api/get_cdb_menu', {
                        cdb: ( typeof v === 'number' ? main_page.cdb.content[v + (Math.abs(main_page.page.count) - 1) * 10] : v)
                    });
                    opening_cdb.value = response.data[0][0];
                    emit.card_page.cdb_opened.to(response.data);
                    data = response.data;
                } catch (error) {}
                return data;
            } as (v : string | number) => Promise<any[]>
        },
        show_list : {
            cdb: true,
            card: false
        },
        uploading : false,
        get : async function () {
            try {
                let response = await axios.get('http://127.0.0.1:8000/api/get_cdbs');
                main_page.cdb.content = response.data;
                main_page.page.count = main_page.cdb.content.length > 0 ? Math.ceil(main_page.cdb.content.length / 10) : 0;
            } catch (error) {}
        } as () => Promise<void>,
        add : async function () {
            try {
                let response = await axios.post('http://127.0.0.1:8000/api/create_new_cdb');
                main_page.get();
            } catch (error) {}
        } as () => Promise<void>,
        remove : async function (cdb) {
            main_page.cdb.content.splice(main_page.cdb.content.indexOf(cdb), 1);
            if (Math.ceil(main_page.cdb.content.length / 10) < main_page.page.count)
                main_page.page.count = Math.ceil(main_page.cdb.content.length / 10);
            await axios.post('http://127.0.0.1:8000/api/remove_file', {file: cdb});
            main_page.show();
        } as (i: string) => Promise<void>,
        show : async function (v = -1, i = new Map().set('cdb', '')) { 
            if (main_page.show_list.card) {
                main_page.show_list.card = false;
                emit.card_page.cdb_closed.to();
                await (new Promise(resolve => setTimeout(resolve, 500)));
                main_page.show_list.cdb = true;
            } else {
                let data = await main_page.cdb.get(v);
                main_page.show_list.cdb = false;
                await (new Promise(resolve => setTimeout(resolve, 500)));
                main_page.show_list.card = true;
                await (new Promise(resolve => setTimeout(resolve, 5)));
                emit.list_page.cdb_opened.to(data);
                emit.list_page.send_select.to();
            }
        } as (v ?: number, i ?: Map<string, any>) => Promise<void>
    });

    let upload_file_input = ref(null);
    let upload_file = {
        click : function (e) {
            try {
                let files = e.target.files;
                if (files.length > 0) {
                    let formData = new FormData();
                    let size = 0;
                    let count = 0;
                    for (let i = 0; i < files.length; i++) {
                        let file = files[i];
                        if (!upload_file.check(file.type, file.name)) {
                            continue;
                        }
                        formData.append('files[]', file);
                        count ++;
                        size += file.size;
                        if (size >= 1024 * 1024 * 10 || count >= 100) {
                            upload_file.send(formData);
                            formData = new FormData();
                            size = 0;
                            count = 0;
                        }
                    }
                    upload_file.send(formData);
                }
            } catch (error) { console.error(error); }
        } as (e: any) => void,
        drag : function (e) {
            let files = e.dataTransfer.files;
            if (files.length > 0) {
                let formData = new FormData();
                let size = 0;
                let count = 0;
                for (let i = 0; i < files.length; i++) {
                    let file = files[i];
                    if (!upload_file.check(file.type, file.name)) {
                        continue;
                    }
                    formData.append('files[]', file);
                    count ++;
                    size += file.size;
                    if (size >= 1024 * 1024 * 10 || count >= 100) {
                        upload_file.send(formData);
                        formData = new FormData();
                        size = 0;
                        count = 0;
                    }
                }
                upload_file.send(formData);
            }
            main_page.uploading = false;
        } as (e: any) => void,
        check : function (type, name) {
            if (type.includes('image') || type.includes('text'))
                return true;
            else if (name.endsWith('.cdb') || name.endsWith('.ypk') || name.endsWith('.zip') || name.endsWith('.tar') || name.endsWith('.tgz') || name.endsWith('.tar.gz') || name.endsWith('.7z') || name.endsWith('.rar') || name.endsWith('.lua'))
                return true;
            
            return false;
        } as (type: string, name: string) => boolean,
        send : async function (formData) {
            try {
                let response = await axios.post('http://127.0.0.1:8000/api/get_file', formData);
                for (let i = 0; i < response.data.length; i++) {
                    if (response.data[i].endsWith('.cdb')) {
                        main_page.cdb.content.push(response.data[i]);
                    }
                }
                if (Math.ceil(main_page.cdb.content.length / 10) > main_page.page.count) {
                    main_page.page.count = Math.ceil(main_page.cdb.content.length / 10);
                }
            } catch (error) {}
        } as (formData: FormData) => Promise<void>
    }

    onMounted(() => {
        main_page.get();
    });

    let emit = {
        card_page: {
            cdb_closed: {
                to : function () {
                    emitter.emit('to_cpage_cdb_closed');
                } as () => void
            },
            cdb_opened: {
                to : function (cdb) {
                    emitter.emit('to_cpage_cdb_opened', cdb);
                } as (cdb: any[]) => void
            }
        },
        list_page: {
            send_select: {
                group : [],
                to : function () {
                    let j = emit.list_page.send_select.group.findIndex(select => select.get('cdb') == opening_cdb.value);
                    if ( j > -1 ) {
                        emitter.emit('to_lpage_send_select', emit.list_page.send_select.group[j]);
                        emit.list_page.send_select.group.splice(j, 1);
                    } else {
                        emitter.emit('to_lpage_send_select', new Map().set('page', -1).set('card', -1));
                    }
                },
                on : function (i) {
                    let j = emit.list_page.send_select.group.findIndex(select => select.get('cdb') == i.get('cdb'));
                    if ( j > -1 ) {
                        emit.list_page.send_select.group[j] = i;
                    } else {
                        emit.list_page.send_select.group.push(i);
                    }
                },
                remove : function (i) {
                    let j = emit.list_page.send_select.group.findIndex(select => select.get('cdb') == i);
                    if ( j > -1 ) {
                        emit.list_page.send_select.group.splice(j, 1);
                    }
                }
            },
            cdb_opened: {
                to : function (cdb) {
                    emitter.emit('to_lpage_cdb_opened', cdb);
                } as (cdb: any[]) => void
            }
        },
        pic : {
            
        }
    }

    emitter.on('to_mpage_send_select', emit.list_page.send_select.on);
    emitter.on('to_mpage_remove_select', emit.list_page.send_select.remove);
</script>

<style scoped>
    .main_page {
        display: flex;
        justify-content: space-between;
    }

    #main_page_left {
        width: 30vw;
        height: 100vh;
    }

    #under_list_page {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    #cdb_list {
        width: 30vw;
        height: 80vh;
    }

    #cdb_list button {
        display: grid;
        align-items:  center;

        width: 30vw;
        height: 8vh;

        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        cursor: pointer;
    }

    #cdb_list button:hover {
        width: 31vw;
        color: white;
        background-color: green;
    }

    #upload_area, #add_area {
        border: 2px dashed #bbbbbb;

        color: #bbbbbb;

        text-align: center;

        cursor: pointer;
    }

    #upload_area {
        width: 25vw;
        height: 10vh;
    }

    #add_area {
        width: 5vw;
        height: 10vh;
    }

    #upload_area:hover, #add_area:hover {
        border: 2px dashed black;
        color: black;
    }

    .cdb_list_btn {
        display: flex;
        align-items:  center;
    }

    .cdb_list_btn button {
        width: 10vw;
        height: 8vh;
        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        cursor: pointer;
    }

    .cdb_list_btn span {
        width: 10vw;
        height: 8vh;
        text-align: center;
    }

    .cdb_list_btn input {
        width: 3vw;
    }

    .slide_list_page-enter-active,
    .slide_list_page-leave-active {
        transition: transform 0.5s ease;
    }

    .slide_list_page-enter-from,
    .slide_list_page-leave-to {
        transform: translateX(-100%);
    }

    .slide_list_page-enter-to,
    .slide_list_page-leave-from {
        transform: translateX(0%);
    }

    .under_list_page-enter-active,
    .under_list_page-leave-active {
        transition: transform 0.5s ease;
    }

    .under_list_page-enter-from,
    .under_list_page-leave-to {
        transform: translateX(-100%);
    }

    .under_list_page-enter-to,
    .under_list_page-leave-from {
        transform: translateX(0%);
    }
</style>