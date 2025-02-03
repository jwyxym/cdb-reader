<template>
    <div class = "list_page">
        <div class = "list_header">
            <h1>{{ select.cdb }}</h1>
            <div>
                <el-button @click = "show.unshow()">
                    <el-icon><Fold/></el-icon>
                </el-button>
                <el-button @click = "show.close()">
                    <el-icon><Delete/></el-icon>
                </el-button>
            </div>
        </div>
        <div class = "list_content">
            <button v-for = "(i,v) in cdb.list[page.count]":key = "v"
                @click = "select.set(v)"
                :style="{
                    'border': select.page == page.count && select.card == v ? '0.01px solid #409eff' : '',
                    'background-color': select.page == page.count && select.card == v ? '#ecf5ff' : '',
                    'color': select.page == page.count && select.card == v ? '#409eff' : ''
                    }"
            >{{ i }}</button>
        </div>
        <div class = "list_btn">
            <el-button @click = "page.previous">上一页</el-button>
            <span>第<input @input = "page.filter($event)" v-model = "page.count" ref = "page.btn"/>页<br>共{{ cdb.list.length - 1 }}页</span>
            <el-button @click = "page.next">下一页</el-button>
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
            emit.card_page.select_card.to();
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
                        select.id = cdb.list[select.page][select.card].split(' ')[0];
                        emit.card_page.select_card.to();
                } as (i: Map<string, number>) => void,
                remove : function (cdb: string) {
                    emitter.emit('to_mpage_remove_select', cdb);
                } as (cdb: string) => void
            }
        },
        card_page : {
            select_card : {
                to : function () {
                    emitter.emit('to_cpage_send_select', new Map().set('id', select.id));
                } as () => void
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
                        if (id == -1)
                            id = select.id;
                        if (id > -1) {
                            response.data.some((page, p) => {
                                return page.some((card, c) => {
                                    if (card.split(' ')[0] == id) {
                                        select.page = p;
                                        page.count = p;
                                        select.card = c;
                                        select.id = card.split(' ')[0];
                                        return true;
                                    }
                                    return false;
                                });
                            });
                        }
                        cdb.list = response.data;
                        select.cdb = response.data[0][0];
                        emit.card_page.cdb_changed.to();
                        emit.card_page.select_card.to();
                    } catch (error) {}
                } as (id ?: number) => Promise<void>
            },
            get_over : {
                on : function () {
                    wait.save_get = true;
                } as () => void
            },
            search : {
                on : async function (i) {
                    try {
                        let response = await axios.post('http://127.0.0.1:8000/api/search_cdb', {
                            keyword : i,
                            cdb: select.cdb
                        });
                        cdb.list = response.data;
                        page.count = 1;
                        select.page = -1;
                        select.card = -1;
                    } catch (error) {}
                } as (i : any[]) => Promise<void>
            }
        },
        remove : function () {
            emitter.off('to_lpage_cdb_opened', emit.mainpage.cdb_opened.on);
            emitter.off('to_lpage_send_select', emit.mainpage.send_select.on);
            emitter.off('to_lpage_card_changed', emit.card_page.card_changed.on);
            emitter.off('to_lpage_cdb_changed', emit.card_page.cdb_changed.on);
            emitter.off('to_lpage_get_over', emit.card_page.get_over.on);
            emitter.off('to_lpage_search', emit.card_page.search.on);
        } as () => void
    }

    emitter.on('to_lpage_cdb_opened', emit.mainpage.cdb_opened.on);
    emitter.on('to_lpage_send_select', emit.mainpage.send_select.on);
    emitter.on('to_lpage_card_changed', emit.card_page.card_changed.on);
    emitter.on('to_lpage_cdb_changed', emit.card_page.cdb_changed.on);
    emitter.on('to_lpage_get_over', emit.card_page.get_over.on);
    emitter.on('to_lpage_search', emit.card_page.search.on);

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
        justify-self: left;
    }

    .list_header div {
        grid-column-start: 4;
        grid-column-end: 5;
        grid-row-start: 1;
        grid-row-end: 3;
        display: grid;
        justify-items: right;
    }

    .list_content {
        height: 80vh;
    }

    .list_content button {
        display: grid;
        align-items:  center;

        width: 30vw;
        height: 8vh;
        border: 0.01px solid #dcdfe6;
        background-color: white;
        color : #606266;
        border-radius: 4px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        cursor: pointer;
    }

    .list_content button:hover {
        width: 31vw;
        color: #409eff;
        background-color: #ecf5ff;
        border: 0.01px solid #409eff;
    }

    .list_btn {
        display: flex;
        align-items:  center;
    }

    .list_btn button {
        width: 10vw;
        height: 8vh;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
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