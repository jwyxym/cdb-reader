<template>
    <img class = "pic" :src = "url_blob" />
</template>
<script setup name = 'pic' lang = 'js'>
    import { ref, reactive, watch, onMounted, computed } from 'vue';
    import axios from 'axios';
    import emitter from '@/utils/emitter';
    import { FieldCenterCard, RushDuelCard, YugiohBackCard, YugiohCard, YugiohSeries2Card } from 'yugioh-card';
    onMounted(() => {
        exportImage();
    })

    let url_blob = ref(null);
    async function exportImage(card, card_count) {
        console.log(card, card_count);
        if(!card||!card_count)return;
        let card_type = 'monster';
        let card_Type = 'normal';
        let pendulum_scale = 0;
        let pendulum_type = 'normal-pendulum';
        let card_icon = '';
        let arrows = [];
        if(card_count.type & 16777216){
            card_type = 'pendulum';
            if(card_count.type & 32){
                pendulum_type = 'effect-pendulum';
            }
            else if(card_count.type & 128){
                pendulum_type = 'ritual-pendulum';
            }
            else if(card_count.type & 64){
                pendulum_type = 'fusion-pendulum';
            }
            else if(card_count.type & 8192){
                pendulum_type = 'synchro-pendulum';
            }
            else if(card_count.type & 8388608){
                pendulum_type = 'xyz-pendulum';
            }
        }
        else if(card_count.type & 1){
            card_type = 'monster';
            if(card_count.type & 32){
                card_Type = 'effect';
            }
            else if(card_count.type & 128){
                card_Type = 'ritual';
            }
            else if(card_count.type & 64){
                card_Type = 'fusion';
            }
            else if(card_count.type & 8192){
                card_Type = 'synchro';
            }
            else if(card_count.type & 8388608){
                card_Type = 'xyz';
            }
            else if(card_count.type & 67108864){
                card_Type = 'link';
                if(card_count.def & 128){
                    arrows.push(1);
                }
                else if(card_count.def & 256){
                    arrows.push(2);
                }
                else if(card_count.def & 32){
                    arrows.push(3);
                }
                else if(card_count.def & 4){
                    arrows.push(4);
                }
                else if(card_count.def & 2){
                    arrows.push(5);
                }
                else if(card_count.def & 1){
                    arrows.push(6);
                }
                else if(card_count.def & 8){
                    arrows.push(7);
                }
                else if(card_count.def & 64){
                    arrows.push(8);
                }
            }
            else if(card_count.type & 16384){
                card_Type = 'token';
            }
        }
        else if(card_count.type & 2){
            card_type = 'spell';
            if(card_count.type & 262144){
                card_icon = 'equip';
            }
            else if(card_count.type & 524288){
                card_icon = 'field';
            }
            else if(card_count.type & 65536){
                card_icon = 'quick-play';
            }
            else if(card_count.type & 128){
                card_icon = 'ritual';
            }
            else if(card_count.type & 131072){
                card_icon = 'continuous';
            }
        }
        else if(card_count.type & 4){
            card_type = 'trap';
            if(card_count.type & 131072){
                card_icon = 'continuous';
            }
            else if(card_count.type & 1048576){
                card_icon = 'counter';
            }
        }
        let card_attribute = '';
        if(card_count.attribute & 32){
            card_attribute = 'dark';
        }
        else if(card_count.attribute & 16){
            card_attribute = 'light';
        }
        else if(card_count.attribute & 1){
            card_attribute = 'earth';
        }
        else if(card_count.attribute & 2){
            card_attribute = 'water';
        }
        else if(card_count.attribute & 4){
            card_attribute = 'fire';
        }
        else if(card_count.attribute & 8){
            card_attribute = 'wind';
        }
        else if(card_count.attribute & 64){
            card_attribute = 'divine';
        }
        let cardLeaf = new YugiohCard({
            data: {
                language: 'sc',
                font: '',
                name: card.name,
                color: '',
                align: 'left',
                gradient: false,
                gradientColor1: '#999999',
                gradientColor2: '#ffffff',
                type: card_type,
                attribute: card_attribute,
                icon: card_icon,
                image: './赌上你的灵魂.png',  // to be continued
                cardType: card_Type,
                pendulumType: pendulum_type,
                level: card_count.level&65535,
                rank: card_count.level&65535,
                pendulumScale: card.pendulum,
                pendulumDescription: '', // to be continued
                monsterType: '龙族/通常', // to be continued
                atkBar: true,
                atk: card_count.atk,
                def: card_count.def,
                arrowList: arrows,
                description: '以高攻击力著称的传说之龙。任何对手都能将之粉碎，其破坏力不可估量。',// to be continued
                firstLineCompress: false,
                descriptionAlign: false,
                descriptionZoom: 1,
                descriptionWeight: 0,
                package: '',
                password: card_count.origin_id,
                copyright: '',
                laser: '',
                rare: '',
                twentieth: false,
                radius: true,
                scale: 1,
            },
            resourcePath: './yugioh-card',
        });
        let formData = new FormData();
        await cardLeaf.leafer.export('jpg', true).then(result => { 
            formData.append('file', result.data, 'blue-eyes.jpg');
            url_blob.value = URL.createObjectURL(result.data);
        })
        await axios.post('http://127.0.0.1:8000/api/get_pics', formData)
    }
    emitter.on('exportImage', (obj)=>{
        exportImage(obj.data1, obj.data2);
    });
</script>