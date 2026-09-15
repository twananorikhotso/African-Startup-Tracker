package com.africa.backend.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

@Entity
@Table(name = "startups")
public class Startup {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @NotBlank(message = "Company name is required")
    @Column(name = "company_name", nullable = false)
    private String company;

    @NotBlank(message = "Country is required")
    @Column(name = "origin_country", nullable = false)
    private String country;

    @NotBlank(message = "Sector is required")
    @Column(name = "target_sector", nullable = false)
    private String sector;

    @NotNull(message = "Funding amount is required")
    @Min(value = 0, message = "Funding amount cannot be negative")
    @Column(name = "funding_amount", nullable = false)
    private Long funding;

    public Startup() {
    }

    public Startup(String company, String country, String sector, Long funding) {
        this.company = company;
        this.country = country;
        this.sector = sector;
        this.funding = funding;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getCompany() {
        return company;
    }

    public void setCompany(String company) {
        this.company = company;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public String getSector() {
        return sector;
    }

    public void setSector(String sector) {
        this.sector = sector;
    }

    public Long getFunding() {
        return funding;
    }

    public void setFunding(Long funding) {
        this.funding = funding;
    }
}