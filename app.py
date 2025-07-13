# 유해요인조사표 탭에 작업명 등 자동 반영 코드

def display_hazard_investigation_tab():
    """유해요인조사표 탭 표시 - 작업목록표의 데이터 자동 반영"""
    st.header("3. 유해요인조사표")
    
    # 작업목록표에서 입력된 데이터 가져오기
    if 'work_list' not in st.session_state or not st.session_state.work_list:
        st.warning("먼저 작업목록표에서 작업을 등록해주세요.")
        return
    
    # 작업 선택 드롭다운
    work_names = [work.get('작업명', f'작업 {idx+1}') for idx, work in enumerate(st.session_state.work_list)]
    selected_work_idx = st.selectbox(
        "조사할 작업 선택",
        range(len(work_names)),
        format_func=lambda x: work_names[x]
    )
    
    # 선택된 작업 정보
    selected_work = st.session_state.work_list[selected_work_idx]
    
    # 작업 정보 자동 표시
    st.markdown("### 작업 정보")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.text_input("작업명", value=selected_work.get('작업명', ''), disabled=True, key=f"hazard_work_name_{selected_work_idx}")
        st.text_input("공정명", value=selected_work.get('공정명', ''), disabled=True, key=f"hazard_process_name_{selected_work_idx}")
    
    with col2:
        st.text_input("부서명", value=selected_work.get('부서', ''), disabled=True, key=f"hazard_dept_{selected_work_idx}")
        st.text_input("작업자수", value=str(selected_work.get('작업자수', '')), disabled=True, key=f"hazard_worker_count_{selected_work_idx}")
    
    with col3:
        st.text_input("유해요인", value=selected_work.get('유해요인', ''), disabled=True, key=f"hazard_risk_factor_{selected_work_idx}")
        st.text_input("작업주기", value=selected_work.get('작업주기', ''), disabled=True, key=f"hazard_work_cycle_{selected_work_idx}")
    
    st.divider()
    
    # 유해요인조사 항목 초기화
    if f'hazard_investigation_{selected_work_idx}' not in st.session_state:
        st.session_state[f'hazard_investigation_{selected_work_idx}'] = {
            '작업명': selected_work.get('작업명', ''),
            '부서': selected_work.get('부서', ''),
            '공정명': selected_work.get('공정명', ''),
            '작업자수': selected_work.get('작업자수', ''),
            '유해요인': selected_work.get('유해요인', ''),
            '작업주기': selected_work.get('작업주기', ''),
            '조사항목': []
        }
    
    investigation_data = st.session_state[f'hazard_investigation_{selected_work_idx}']
    
    # 유해요인 조사 섹션
    st.markdown("### 유해요인 세부 조사")
    
    # 부담작업 체크리스트
    st.markdown("#### 부담작업 해당 여부")
    
    burden_work_items = [
        "(1호) 하루에 4시간 이상 집중적으로 자료입력 등을 위해 키보드 또는 마우스를 조작하는 작업",
        "(2호) 하루에 총 2시간 이상 목, 어깨, 팔꿈치, 손목 또는 손을 사용하여 같은 동작을 반복하는 작업",
        "(3호) 하루에 총 2시간 이상 머리 위에 손이 있거나, 팔꿈치가 어깨위에 있거나, 팔꿈치를 몸통으로부터 들거나, 팔꿈치를 몸통뒤쪽에 위치하도록 하는 상태에서 이루어지는 작업",
        "(4호) 지지되지 않은 상태이거나 임의로 자세를 바꿀 수 없는 조건에서, 하루에 총 2시간 이상 목이나 허리를 구부리거나 트는 상태에서 이루어지는 작업",
        "(5호) 하루에 총 2시간 이상 쪼그리고 앉거나 무릎을 굽힌 자세에서 이루어지는 작업",
        "(6호) 하루에 총 2시간 이상 지지되지 않은 상태에서 1kg 이상의 물건을 한손의 손가락으로 집어 옮기거나, 2kg 이상에 상응하는 힘을 가하여 한손의 손가락으로 물건을 쥐는 작업",
        "(7호) 하루에 총 2시간 이상 지지되지 않은 상태에서 4.5kg 이상의 물건을 한 손으로 들거나 동일한 힘으로 쥐는 작업",
        "(8호) 하루에 10회 이상 25kg 이상의 물체를 드는 작업",
        "(9호) 하루에 25회 이상 10kg 이상의 물체를 무릎 아래에서 들거나, 어깨 위에서 들거나, 팔을 뻗은 상태에서 드는 작업",
        "(10호) 하루에 총 2시간 이상, 분당 2회 이상 4.5kg 이상의 물체를 드는 작업",
        "(11호) 하루에 총 2시간 이상 시간당 10회 이상 손 또는 무릎을 사용하여 반복적으로 충격을 가하는 작업"
    ]
    
    # 체크박스로 부담작업 선택
    selected_burden_works = []
    cols = st.columns(2)
    for idx, item in enumerate(burden_work_items):
        with cols[idx % 2]:
            if st.checkbox(item, key=f"burden_check_{selected_work_idx}_{idx}"):
                selected_burden_works.append(item)
    
    # 추가 조사 항목
    st.markdown("#### 추가 조사 항목")
    
    col1, col2 = st.columns(2)
    
    with col1:
        작업_내용 = st.text_area(
            "주요 작업 내용",
            value=investigation_data.get('작업_내용', ''),
            height=100,
            key=f"hazard_work_content_{selected_work_idx}"
        )
        
        사용_도구 = st.text_area(
            "사용 도구 및 설비",
            value=investigation_data.get('사용_도구', ''),
            height=100,
            key=f"hazard_tools_{selected_work_idx}"
        )
    
    with col2:
        작업_시간 = st.text_input(
            "1일 총 작업시간(시간)",
            value=investigation_data.get('작업_시간', ''),
            key=f"hazard_work_time_{selected_work_idx}"
        )
        
        휴식_시간 = st.text_input(
            "작업 중 휴식시간(분)",
            value=investigation_data.get('휴식_시간', ''),
            key=f"hazard_rest_time_{selected_work_idx}"
        )
        
        작업_빈도 = st.text_input(
            "작업 빈도(회/일)",
            value=investigation_data.get('작업_빈도', ''),
            key=f"hazard_frequency_{selected_work_idx}"
        )
    
    # 신체 부위별 부담 정도
    st.markdown("#### 신체 부위별 부담 정도")
    
    body_parts = ["목", "어깨", "팔/팔꿈치", "손/손목/손가락", "허리", "다리/무릎"]
    burden_levels = ["없음", "약간", "보통", "심함", "매우 심함"]
    
    body_burden_data = {}
    cols = st.columns(len(body_parts))
    
    for idx, part in enumerate(body_parts):
        with cols[idx]:
            st.write(f"**{part}**")
            level = st.radio(
                "부담 정도",
                burden_levels,
                key=f"body_burden_{selected_work_idx}_{part}",
                label_visibility="collapsed"
            )
            body_burden_data[part] = level
    
    # 특이사항
    st.markdown("#### 특이사항 및 작업자 의견")
    특이사항 = st.text_area(
        "특이사항",
        value=investigation_data.get('특이사항', ''),
        height=100,
        key=f"hazard_special_notes_{selected_work_idx}"
    )
    
    # 데이터 저장
    if st.button("유해요인조사 저장", key=f"save_hazard_investigation_{selected_work_idx}"):
        investigation_data.update({
            '선택된_부담작업': selected_burden_works,
            '작업_내용': 작업_내용,
            '사용_도구': 사용_도구,
            '작업_시간': 작업_시간,
            '휴식_시간': 휴식_시간,
            '작업_빈도': 작업_빈도,
            '신체부위별_부담': body_burden_data,
            '특이사항': 특이사항,
            '조사일시': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        st.session_state[f'hazard_investigation_{selected_work_idx}'] = investigation_data
        st.success(f"'{selected_work.get('작업명', '')}'의 유해요인조사가 저장되었습니다.")
    
    # 조사 완료된 작업 표시
    st.divider()
    st.markdown("### 조사 완료 현황")
    
    completed_investigations = []
    for idx, work in enumerate(st.session_state.work_list):
        if f'hazard_investigation_{idx}' in st.session_state:
            inv_data = st.session_state[f'hazard_investigation_{idx}']
            if '조사일시' in inv_data:
                completed_investigations.append({
                    '작업명': work.get('작업명', ''),
                    '부서': work.get('부서', ''),
                    '조사일시': inv_data.get('조사일시', ''),
                    '부담작업수': len(inv_data.get('선택된_부담작업', []))
                })
    
    if completed_investigations:
        df_completed = pd.DataFrame(completed_investigations)
        st.dataframe(df_completed, use_container_width=True)
    else:
        st.info("아직 조사 완료된 작업이 없습니다.")


# 데이터 연동 함수
def sync_work_data_to_hazard_investigation():
    """작업목록표 데이터가 변경될 때 유해요인조사표에 자동 반영"""
    if 'work_list' not in st.session_state:
        return
    
    # 각 작업에 대해 기본 정보 동기화
    for idx, work in enumerate(st.session_state.work_list):
        if f'hazard_investigation_{idx}' in st.session_state:
            # 기존 조사 데이터가 있으면 작업 정보만 업데이트
            st.session_state[f'hazard_investigation_{idx}'].update({
                '작업명': work.get('작업명', ''),
                '부서': work.get('부서', ''),
                '공정명': work.get('공정명', ''),
                '작업자수': work.get('작업자수', ''),
                '유해요인': work.get('유해요인', ''),
                '작업주기': work.get('작업주기', '')
            })


# 메인 앱에서 사용
def main():
    # ... 기존 코드 ...
    
    # 탭 생성
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "체크리스트", "작업목록표", "유해요인조사표", 
        "작업조건조사", "정밀평가", "개선대책"
    ])
    
    with tab1:
        # 체크리스트 탭 내용
        pass
    
    with tab2:
        # 작업목록표 탭 내용
        # 작업 정보가 변경되면 유해요인조사표에 자동 반영
        sync_work_data_to_hazard_investigation()
    
    with tab3:
        # 유해요인조사표 탭
        display_hazard_investigation_tab()
    
    # ... 나머지 탭들 ...