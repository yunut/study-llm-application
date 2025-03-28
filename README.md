# RAG (Retrieval-Augmented Generation) 학습 프로젝트

이 프로젝트는 RAG(Retrieval-Augmented Generation) 기술을 학습하고 구현하기 위한 예제 코드입니다.

## 프로젝트 구조

- `1. langchain_llm_test.ipynb`: LangChain과 OpenAI를 사용한 기본 LLM 테스트
- `2. rag_with_chroma copy.ipynb`: ChromaDB를 사용한 RAG 구현
- `3. rag_without_langchain_with_chroma.ipynb`: LangChain 없이 ChromaDB만 사용한 RAG 구현
- `4. rag_with_pinecone copy 2.ipynb`: Pinecone을 사용한 RAG 구현
- `5. rag_with_pinecone_improve copy.ipynb`: Pinecone을 사용한 개선된 RAG 구현
- `app.py`: Streamlit을 사용한 웹 인터페이스
- `llm.py`: RAG와 Few-shot 학습을 구현한 핵심 로직
- `config.py`: 설정 파일

## 주요 기능

1. 문서 처리
   - PDF 파일 로드 (PyPDFLoader)
   - Word 문서 로드 (Docx2txtLoader)
   - 문서 청크 분할 (RecursiveCharacterTextSplitter)

2. 임베딩
   - OpenAI Embeddings 사용
   - 텍스트 벡터화

3. 벡터 데이터베이스
   - ChromaDB (로컬 벡터 DB)
   - Pinecone (클라우드 벡터 DB)

4. 고급 기능
   - Few-shot 학습을 통한 답변 품질 향상
   - 대화 히스토리 기반 컨텍스트 이해
   - 사용자 정의 사전을 통한 질문 전처리
   - Streamlit을 활용한 인터랙티브 웹 인터페이스

## 환경 설정

1. 필요한 패키지 설치:
```bash
pip install langchain-openai python-dotenv chromadb pinecone-client docx2txt streamlit
```

2. 환경 변수 설정 (.env 파일):
```
OPENAI_API_KEY=your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-pinecone-environment
```

## 사용 방법

1. Jupyter Notebook 실행
   - 각 노트북의 순서대로 실행하여 RAG의 다양한 구현 방식을 학습
   - 문서 처리, 임베딩, 벡터 DB 저장 및 검색 과정 확인

2. Streamlit 앱 실행
   ```bash
   streamlit run app.py
   ```
   - 웹 인터페이스를 통해 소득세 관련 질문에 대한 답변 받기
   - 대화 히스토리 확인
   - Few-shot 학습을 통한 정확한 답변 확인

## 주의사항

- PDF 파일의 경우 이미지나 표가 포함된 경우 정확한 텍스트 추출이 어려울 수 있습니다
- Pinecone 사용 시 인덱스 생성이 필요합니다
- API 키는 반드시 .env 파일에 안전하게 저장해야 합니다
- Few-shot 학습의 예제는 config.py에서 관리됩니다
