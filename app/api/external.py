from fastapi import APIRouter, HTTPException, Query

from app.services.scraping_service import ExchangeRateScraper

router = APIRouter(prefix="/external", tags=["external-data"])


@router.get("/exchange-rate")
def get_exchange_rate(
    base: str = Query(default="USD", min_length=3, max_length=3),
    target: str = Query(default="EUR", min_length=3, max_length=3),
):
    try:
        result = ExchangeRateScraper.fetch_rate(base=base, target=target)
        return {
            "base": result.base,
            "target": result.target,
            "rate": result.rate,
            "source": result.source,
        }
    except (ValueError, LookupError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
