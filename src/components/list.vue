<template>
    <div class = "list_page">
        <div class = "list_header">
            <h1>{{ select.cdb }}</h1>
            <button id = "unshow_list_page_btn" @click = "show.unshow()" title = "上一级目录">&lt;</button>
            <button id = "close_cdb_btn" @click = "show.close()" title = "关闭cdb">&times;</button>
        </div>
        <div class = "list_content">
            <button v-for = "(i,v) in cdb.list[page.count]":key = "v"
                @click = "select.set(v)"
                :style="{
                    'background-color': select.page == page.count && select.card == v ? 'green' : '',
                    'color': select.page == page.count && select.card == v ? 'white' : ''
                    }"
            >{{ i }}</button>
        </div>
        <div class = "list_btn">
            <button @click = "page.previous"
                :style = "{ 'background-color': page.count <= 1 ? 'gray' : 'green', 'color': page.count <= 1 ? 'black' : 'white' }"
            >上一页</button>
            <span>第<input @input = "page.filter($event)" v-model = "page.count" ref = "page.btn"/>页<br>共{{ cdb.list.length - 1 }}页</span>
            <button @click = "page.next()"
                :style = "{ 'background-color': page.count >= cdb.list.length - 1 ? 'gray' : 'green', 'color': page.count >= cdb.list.length - 1 ? 'black' : 'white' }"
            >下一页</button>
        </div>
    </div>
</template>

<script setup name="list_page" lang = "ts">
    import { ref, reactive, onMounted, watch, defineEmits, defineProps, computed } from 'vue';
    import axios from 'axios';
    import emitter from '@/utils/emitter';

    let cdb = reactive({
        list : []
    });

    let wait = {
        save_get : true
    }

    let select = reactive({
        cdb : '',
        id : -1,
        page : -1,
        card : -1,
        set : function (v) {
            if (!wait.save_get) return;
            wait.save_get = false;
            if (select.page != page.count || select.card != v) {
                select.page = page.count;
                select.card = v;
                select.id = cdb.list[page.count][v].split(' ')[0];
            } else {
                select.page = -1;
                select.card = -1;
                select.id = -1;
            }
            emit.card_page.select_card.to(v);
        } as (v: number) => void
    });

    let show = reactive({
        unshow : function () {
            emit.remove();
            emit.mainpage.send_select.to();
            emit.mainpage.cdb_unshow.to();
        } as () => void,
        close : function () {
            if (confirm('确认关闭cdb吗，此操作可能导致数据丢失')) {
                emit.remove();
                emit.mainpage.send_select.remove(select.cdb);
                emit.mainpage.cdb_closed.to();
            }
        } as () => void
    });

    let page = reactive({
        count : 0,
        btn : ref(null),
        next : function () {
            if (page.count < cdb.list.length - 1)
                page.count ++ ;
        } as () => void,
        previous : function () {
            if (page.count > 1)
                page.count -- ;
        } as () => void,
        filter : function (event) {
            let input_value = event.target.value;
            let new_value = input_value.replace(/[^0-9]/, '');
            while (parseInt(new_value) > (cdb.list.length - 1))
                new_value = new_value.slice(0, -1);
            if (new_value == '')
                new_value = 0;
            if (parseInt(new_value) < 1 && cdb.list.length > 1)
                new_value = 1;
            page.count = new_value;
        }
    });

    let em = defineEmits(['event_close_cdb', 'event_unshow_list_page'])

    let emit = {
        mainpage : {
            cdb_unshow : {
                to : function () {
                    em('event_unshow_list_page');
                }
            },
            cdb_closed : {
                to : function () {
                    em('event_close_cdb', select.cdb);
                }
            },
            cdb_opened : {
                on : function (i) {
                    select.cdb = i[0][0];
                    cdb.list = i;
                    page.count = (cdb.list.length > 0 ? 1 : 0);
                } as (i: any[]) => void
            },
            send_select : {
                to : function () {
                    emitter.emit('to_mpage_send_select', new Map().set('cdb', select.cdb).set('page', select.page).set('card', select.card));
                } as () => void,
                on : function (i) {
                    select.card = i.get('card');
                    select.page = i.get('page');
                    if (select.page > -1 && cdb.list.length > select.page)
                        page.count = select.page;
                    if (select.card > -1)
                        emit.card_page.select_card.to(select.card);
                } as (i: Map<string, number>) => void,
                remove : function (cdb: string) {
                    emitter.emit('to_mpage_remove_select', cdb);
                } as (cdb: string) => void
            }
        },
        card_page : {
            select_card : {
                to : function (i) {
                    emitter.emit('to_cpage_send_select', new Map().set('card', i).set('page', page.count));
                } as (i: number) => void
            },
            card_changed : {
                on : function (i) {
                    if (page.count == 0) return;
                    cdb.list[page.count][select.card] = i;
                } as (i: Map<string, any>) => void
            },
            cdb_changed : {
                to : function () {
                    emitter.emit('to_cpage_cdb_changed', cdb.list);
                } as () => void,
                on : async function (id = -1) {
                    try {
                        let response = await axios.post('http://127.0.0.1:8000/api/get_cdb_menu', {
                            cdb: select.cdb
                        });
                        let c = -1;
                        let p = 1;
                        if (id == -1)
                            id = select.id;
                        if (id > -1) {
                            for (let i = 0; i < response.data.length; i++) {
                                for (let j = 0; j < response.data[i].length; j++) {
                                    if (response.data[i][j].split(' ')[0] == (id)) {
                                        p = i;
                                        c = j;
                                        break;
                                    }
                                }
                            }
                        }
                        select.page = p;
                        page.count = p;
                        select.card = c;
                        cdb.list = response.data;
                        select.cdb = response.data[0][0];
                        emit.card_page.cdb_changed.to();
                        emit.card_page.select_card.to(c);
                    } catch (error) {}
                } as (id ?: number) => Promise<void>
            },
            get_over : {
                on : function () {
                    wait.save_get = true;
                } as () => void
            }
        },
        remove : function () {
            emitter.off('to_lpage_cdb_opened', emit.mainpage.cdb_opened.on);
            emitter.off('to_lpage_send_select', emit.mainpage.send_select.on);
            emitter.off('to_lpage_card_changed', emit.card_page.card_changed.on);
            emitter.off('to_lpage_cdb_changed', emit.card_page.cdb_changed.on);
            emitter.off('to_lpage_get_over', emit.card_page.get_over.on);
        } as () => void
    }

    emitter.on('to_lpage_cdb_opened', emit.mainpage.cdb_opened.on);
    emitter.on('to_lpage_send_select', emit.mainpage.send_select.on);
    emitter.on('to_lpage_card_changed', emit.card_page.card_changed.on);
    emitter.on('to_lpage_cdb_changed', emit.card_page.cdb_changed.on);
    emitter.on('to_lpage_get_over', emit.card_page.get_over.on);

</script>

<style scoped>
    .list_page {
        width: 30vw;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        display: grid;
    }

    .list_header {
        height: 10vh;
        width: 30vw;
        
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-template-rows: repeat(2, 1fr);
    }

    .list_header h1 {
        grid-column-start: 1;
        grid-column-end: 4;
        grid-row-start: 1;
        grid-row-end: 3;
    }

    #unshow_list_page_btn {
        width: 4vw;
        height: 4vh;

        align-self: center;
        justify-self: right;

        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white;
        background-color: green;

        cursor: pointer;
    }

    #close_cdb_btn {
        width: 4vw;
        height: 4vh;

        align-self: center;
        justify-self: right;

        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white;
        background-color: red;

        cursor: pointer;
    }

    .list_content {
        height: 80vh;
    }

    .list_content button {
        display: grid;

        width: 30vw;
        height: 8vh;

        align-items:  center;

        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        cursor: pointer;
    }

    .list_content button:hover {
        width: 31vw;
        color: white;
        background-color: green;
    }

    .list_btn {
        display: flex;
        align-items:  center;
    }

    .list_btn button {
        width: 10vw;
        height: 8vh;
        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        cursor: pointer;
    }

    .list_btn span {
        width: 10vw;
        height: 8vh;
        text-align: center;
    }

    .list_btn input {
        width: 3vw;
    }
</style>