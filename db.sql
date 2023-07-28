--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

-- Started on 2023-07-28 04:11:43

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3337 (class 1262 OID 16562)
-- Name: reply_io_test; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE reply_io_test WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';


ALTER DATABASE reply_io_test OWNER TO postgres;

\connect reply_io_test

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 16697)
-- Name: searches; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.searches (
    search_id integer NOT NULL,
    status integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.searches OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16696)
-- Name: searches_search_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.searches ALTER COLUMN search_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.searches_search_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 217 (class 1259 OID 16703)
-- Name: searches_texts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.searches_texts (
    text_id text NOT NULL,
    search_id integer NOT NULL
);


ALTER TABLE public.searches_texts OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 16664)
-- Name: texts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.texts (
    text_id text NOT NULL,
    description text
);


ALTER TABLE public.texts OWNER TO postgres;

--
-- TOC entry 3185 (class 2606 OID 16702)
-- Name: searches searches_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.searches
    ADD CONSTRAINT searches_pkey PRIMARY KEY (search_id);


--
-- TOC entry 3187 (class 2606 OID 16709)
-- Name: searches_texts searches_texts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.searches_texts
    ADD CONSTRAINT searches_texts_pkey PRIMARY KEY (text_id, search_id);


--
-- TOC entry 3183 (class 2606 OID 16670)
-- Name: texts texts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.texts
    ADD CONSTRAINT texts_pkey PRIMARY KEY (text_id);


--
-- TOC entry 3188 (class 2606 OID 16715)
-- Name: searches_texts fk_searches; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.searches_texts
    ADD CONSTRAINT fk_searches FOREIGN KEY (search_id) REFERENCES public.searches(search_id);


--
-- TOC entry 3189 (class 2606 OID 16710)
-- Name: searches_texts fk_texts; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.searches_texts
    ADD CONSTRAINT fk_texts FOREIGN KEY (text_id) REFERENCES public.texts(text_id);


-- Completed on 2023-07-28 04:11:44

--
-- PostgreSQL database dump complete
--

