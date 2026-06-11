from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Livro
from app.schemas.schemas import LivroCreate, LivroOut
from typing import List

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.post("/", response_model=LivroOut, status_code=201)
def cadastrar_livro(livro: LivroCreate, db: Session = Depends(get_db)):
    """Cadastra um novo livro no sistema."""
    # Verifica ISBN duplicado
    if livro.isbn:
        existente = db.query(Livro).filter(Livro.isbn == livro.isbn).first()
        if existente:
            raise HTTPException(status_code=400, detail="ISBN já cadastrado.")

    novo = Livro(
        titulo=livro.titulo,
        autor=livro.autor,
        ano_publicacao=livro.ano_publicacao,
        isbn=livro.isbn,
        quantidade_total=livro.quantidade_total,
        quantidade_disponivel=livro.quantidade_total,  # inicia igual ao total
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/", response_model=List[LivroOut])
def listar_livros(db: Session = Depends(get_db)):
    """Lista todos os livros cadastrados."""
    return db.query(Livro).all()


@router.get("/disponiveis", response_model=List[LivroOut])
def listar_livros_disponiveis(db: Session = Depends(get_db)):
    """Lista apenas livros com ao menos 1 exemplar disponível."""
    return db.query(Livro).filter(Livro.quantidade_disponivel > 0).all()


@router.get("/{livro_id}", response_model=LivroOut)
def buscar_livro(livro_id: int, db: Session = Depends(get_db)):
    """Busca um livro pelo ID."""
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    return livro
