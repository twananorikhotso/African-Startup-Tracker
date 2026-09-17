package com.africa.backend.controller;

import com.africa.backend.entity.Startup;
import com.africa.backend.exception.GlobalExceptionHandler;
import com.africa.backend.repository.StartupRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(StartupController.class)
class StartupControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private StartupRepository startupRepository;

    @Test
    void getStartupsReturnsStartupData() throws Exception {
        Startup startup = new Startup(
                "Paystack",
                "Nigeria",
                "FinTech",
                200_000_000L
        );
        startup.setId(1);

        when(startupRepository.findAll())
                .thenReturn(List.of(startup));

        mockMvc.perform(get("/startups"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].id").value(1))
                .andExpect(jsonPath("$[0].company").value("Paystack"))
                .andExpect(jsonPath("$[0].country").value("Nigeria"))
                .andExpect(jsonPath("$[0].sector").value("FinTech"))
                .andExpect(jsonPath("$[0].funding").value(200_000_000));
    }

    @Test
    void validPostCreatesStartup() throws Exception {
        Startup startup = new Startup(
                "Flutterwave",
                "Nigeria",
                "Payments",
                170_000_000L
        );

        Startup savedStartup = new Startup(
                "Flutterwave",
                "Nigeria",
                "Payments",
                170_000_000L
        );
        savedStartup.setId(2);

        when(startupRepository.save(any(Startup.class)))
                .thenReturn(savedStartup);

        mockMvc.perform(
                        post("/startups")
                                .contentType(MediaType.APPLICATION_JSON)
                                .content(objectMapper.writeValueAsString(startup))
                )
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(2))
                .andExpect(jsonPath("$.company").value("Flutterwave"))
                .andExpect(jsonPath("$.country").value("Nigeria"))
                .andExpect(jsonPath("$.sector").value("Payments"))
                .andExpect(jsonPath("$.funding").value(170_000_000));
    }

    @Test
    void invalidPostReturnsBadRequest() throws Exception {
        String invalidStartup = """
                {
                    "company": "",
                    "country": "Nigeria",
                    "sector": "FinTech",
                    "funding": 1000000
                }
                """;

        mockMvc.perform(
                        post("/startups")
                                .contentType(MediaType.APPLICATION_JSON)
                                .content(invalidStartup)
                )
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.message")
                        .value("Invalid startup data"));
    }

    @Test
    void negativeFundingReturnsBadRequest() throws Exception {
        String invalidStartup = """
                {
                    "company": "Test Startup",
                    "country": "South Africa",
                    "sector": "FinTech",
                    "funding": -1
                }
                """;

        mockMvc.perform(
                        post("/startups")
                                .contentType(MediaType.APPLICATION_JSON)
                                .content(invalidStartup)
                )
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.message")
                        .value("Invalid startup data"));
    }

    @Test
    void unexpectedRepositoryErrorReturnsInternalServerError()
            throws Exception {

        when(startupRepository.findAll())
                .thenThrow(new RuntimeException("Database unavailable"));

        mockMvc.perform(get("/startups"))
                .andExpect(status().isInternalServerError())
                .andExpect(jsonPath("$.status").value(500))
                .andExpect(jsonPath("$.message")
                        .value("Unable to process request"));
    }
}